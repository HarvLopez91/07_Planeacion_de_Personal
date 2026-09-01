#Requires -Version 5.1
# Actualiza de forma controlada Planta Personal desde Gasto Laboral mediante Excel COM.
[CmdletBinding()]
param(
    [Parameter(Mandatory)] [string] $SourcePath,
    [Parameter(Mandatory)] [string] $TargetPath,
    [string] $OutputPath,
    [Parameter(Mandatory)] [ValidateRange(2000, 2100)] [int] $Year,
    [Parameter(Mandatory)] [ValidateRange(1, 12)] [int] $Month,
    [int] $ExpectedChanges = -1,
    [switch] $DryRun,
    [switch] $AllowReplaceExisting
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Normalize-Label([object] $Value) {
    if ($null -eq $Value) { return $null }
    $decomposed = ([string]$Value).Trim().Normalize([Text.NormalizationForm]::FormD)
    $builder = [Text.StringBuilder]::new()
    foreach ($character in $decomposed.ToCharArray()) {
        if ([Globalization.CharUnicodeInfo]::GetUnicodeCategory($character) -ne [Globalization.UnicodeCategory]::NonSpacingMark) {
            [void]$builder.Append($character)
        }
    }
    return $builder.ToString().Normalize([Text.NormalizationForm]::FormC).ToUpperInvariant()
}

function Get-Sha256([string] $Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
}

function Assert-Unlocked([string] $Path) {
    $stream = $null
    try {
        $stream = [IO.File]::Open($Path, [IO.FileMode]::Open, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None)
    }
    finally {
        if ($stream) { $stream.Dispose() }
    }
}

function Find-HeaderColumn($Worksheet, [int] $HeaderRow, [int] $FirstColumn, [int] $LastColumn, [string] $Header) {
    $wanted = Normalize-Label $Header
    $matches = @()
    for ($column = $FirstColumn; $column -le $LastColumn; $column++) {
        if ((Normalize-Label $Worksheet.Cells.Item($HeaderRow, $column).Value2) -eq $wanted) {
            $matches += $column
        }
    }
    if ($matches.Count -ne 1) {
        throw "Se esperaba un encabezado unico '$Header' entre columnas $FirstColumn y $LastColumn; encontrados: $($matches.Count)."
    }
    return $matches[0]
}

function Find-SourceRow($Worksheet, [int] $CompanyColumn, [string] $Company, [int] $FirstRow, [int] $LastRow) {
    $wanted = Normalize-Label $Company
    $matches = @()
    for ($row = $FirstRow; $row -le $LastRow; $row++) {
        if ((Normalize-Label $Worksheet.Cells.Item($row, $CompanyColumn).Value2) -eq $wanted) {
            $matches += $row
        }
    }
    if ($matches.Count -ne 1) {
        throw "Se esperaba una fila fuente unica para '$Company'; encontradas: $($matches.Count)."
    }
    return $matches[0]
}

if (-not (Test-Path -LiteralPath $SourcePath -PathType Leaf)) { throw "No existe la fuente: $SourcePath" }
if (-not (Test-Path -LiteralPath $TargetPath -PathType Leaf)) { throw "No existe el destino: $TargetPath" }
if ($Year -ne 2026) { throw 'La automatizacion actual solo esta validada para la estructura fuente 2026.' }
if (-not $DryRun -and [string]::IsNullOrWhiteSpace($OutputPath)) { throw 'OutputPath es obligatorio fuera de DryRun.' }
if (-not $DryRun -and (Test-Path -LiteralPath $OutputPath)) { throw "OutputPath ya existe: $OutputPath" }

Assert-Unlocked $SourcePath
Assert-Unlocked $TargetPath

$monthNames = @('', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre')
$monthName = $monthNames[$Month]
$mapping = @(
    [pscustomobject]@{ Source = 'Lemco';          Group = 'Lemco';                Company = 'Lemco';                      HasSales = $true;  Scale = 1 },
    [pscustomobject]@{ Source = 'Habitel';        Group = 'Habitel Hotels';       Company = 'Habitel Nomina Compartida'; HasSales = $true;  Scale = 1 },
    [pscustomobject]@{ Source = 'Lemco Salvio';   Group = 'Habitel Hotels';       Company = 'Lemco Salvio';              HasSales = $true;  Scale = 1 },
    [pscustomobject]@{ Source = 'Operadora';      Group = 'Habitel Hotels';       Company = 'Operadora';                 HasSales = $false; Scale = 1 },
    [pscustomobject]@{ Source = 'Fundacion';      Group = 'Fundacion Challenger'; Company = 'Fundacion Challenger';      HasSales = $true;  Scale = 1 },
    [pscustomobject]@{ Source = 'Challenger';     Group = 'Challenger';           Company = 'Challenger';                HasSales = $true;  Scale = 1000000 },
    [pscustomobject]@{ Source = 'Sky Logistica';  Group = 'Grupo Sky';            Company = 'Sky Logistica Integral';    HasSales = $true;  Scale = 1 },
    [pscustomobject]@{ Source = 'Sky Industrial'; Group = 'Grupo Sky';            Company = 'Sky Industrial';            HasSales = $true;  Scale = 1 },
    [pscustomobject]@{ Source = 'Sky Forwarder';  Group = 'Grupo Sky';            Company = 'Sky Forwarder';             HasSales = $true;  Scale = 1 }
)

$sourceHash = Get-Sha256 $SourcePath
$targetHash = Get-Sha256 $TargetPath
$workingPath = $TargetPath
if (-not $DryRun) {
    $parent = Split-Path -Parent $OutputPath
    if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
    Copy-Item -LiteralPath $TargetPath -Destination $OutputPath
    $workingPath = $OutputPath
}

$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false
$excel.AskToUpdateLinks = $false
$changes = [System.Collections.Generic.List[object]]::new()
$unchanged = [System.Collections.Generic.List[object]]::new()
$sourceNulls = [System.Collections.Generic.List[object]]::new()
$sourceBook = $null
$targetBook = $null

try {
    $sourceBook = $excel.Workbooks.Open($SourcePath, 0, $true)
    $targetBook = $excel.Workbooks.Open($workingPath, 0, [bool]$DryRun)
    try {
        $expenseSheet = $sourceBook.Worksheets.Item('Gasto Laboral Ppto 2026')
        $salesSheet = $sourceBook.Worksheets.Item('Gastos Operacio-Ventas')
        $targetSheet = $targetBook.Worksheets.Item('Planta Personal')

        $requiredHeaders = @('Ppto/Real', 'Ano', 'Mes Num', 'Grupo Empresa', 'Empresa', 'Ventas (MM)', 'Gasto Personal', 'Ppto Ventas (MM)', 'Ppto Gasto Personal')
        $targetHeaders = @{}
        for ($column = 1; $column -le $targetSheet.UsedRange.Columns.Count; $column++) {
            $value = Normalize-Label $targetSheet.Cells.Item(1, $column).Value2
            if ($value) { $targetHeaders[$value] = $column }
        }
        foreach ($header in $requiredHeaders) {
            if (-not $targetHeaders.ContainsKey((Normalize-Label $header))) { throw "Falta columna destino requerida: $header" }
        }

        $expenseActualColumn = Find-HeaderColumn $expenseSheet 3 17 29 $monthName
        $salesActualColumn = Find-HeaderColumn $salesSheet 3 18 30 $monthName
        $salesBudgetColumn = Find-HeaderColumn $salesSheet 3 3 14 $monthName

        $targetRows = @{}
        for ($row = 2; $row -le $targetSheet.UsedRange.Rows.Count; $row++) {
            $rowYear = $targetSheet.Cells.Item($row, $targetHeaders[(Normalize-Label 'Ano')]).Value2
            $rowMonth = $targetSheet.Cells.Item($row, $targetHeaders[(Normalize-Label 'Mes Num')]).Value2
            $rowType = Normalize-Label $targetSheet.Cells.Item($row, $targetHeaders[(Normalize-Label 'Ppto/Real')]).Value2
            if ($rowYear -eq $Year -and $rowMonth -eq $Month -and $rowType -eq 'REAL') {
                $key = '{0}|{1}' -f (Normalize-Label $targetSheet.Cells.Item($row, $targetHeaders[(Normalize-Label 'Grupo Empresa')]).Value2), (Normalize-Label $targetSheet.Cells.Item($row, $targetHeaders[(Normalize-Label 'Empresa')]).Value2)
                if ($targetRows.ContainsKey($key)) { throw "Llave destino duplicada para $key" }
                $targetRows[$key] = $row
            }
        }
        if ($targetRows.Count -ne 12) { throw "Se esperaban 12 filas Real para $Year/$Month; encontradas: $($targetRows.Count)." }

        foreach ($item in $mapping) {
            $key = '{0}|{1}' -f (Normalize-Label $item.Group), (Normalize-Label $item.Company)
            if (-not $targetRows.ContainsKey($key)) { throw "No existe fila destino unica para $key" }
            $targetRow = $targetRows[$key]
            $expenseRow = Find-SourceRow $expenseSheet 16 $item.Source 4 12
            $values = [ordered]@{
                'Gasto Personal' = $expenseSheet.Cells.Item($expenseRow, $expenseActualColumn).Value2
            }
            if ($item.HasSales) {
                $salesActualRow = Find-SourceRow $salesSheet 17 $item.Source 4 11
                $salesBudgetRow = Find-SourceRow $salesSheet 2 $item.Source 4 11
                $values['Ventas (MM)'] = $salesSheet.Cells.Item($salesActualRow, $salesActualColumn).Value2
                $values['Ppto Ventas (MM)'] = $salesSheet.Cells.Item($salesBudgetRow, $salesBudgetColumn).Value2
            }

            foreach ($columnName in $values.Keys) {
                $sourceValue = $values[$columnName]
                if ($null -eq $sourceValue -or [string]::IsNullOrWhiteSpace([string]$sourceValue)) {
                    $sourceNulls.Add([pscustomobject]@{ Company = $item.Company; Column = $columnName })
                    continue
                }
                $expectedValue = [double]$sourceValue * [double]$item.Scale
                $column = $targetHeaders[(Normalize-Label $columnName)]
                $currentValue = $targetSheet.Cells.Item($targetRow, $column).Value2
                if ($null -ne $currentValue -and -not [string]::IsNullOrWhiteSpace([string]$currentValue)) {
                    if ([math]::Abs([double]$currentValue - $expectedValue) -lt 0.001) {
                        $unchanged.Add([pscustomobject]@{ Row = $targetRow; Company = $item.Company; Column = $columnName; Value = $expectedValue })
                        continue
                    }
                    if (-not $AllowReplaceExisting) { throw "La celda $columnName de $($item.Company) contiene un valor diferente y no se autorizo reemplazarlo." }
                }
                $changes.Add([pscustomobject]@{ Row = $targetRow; Company = $item.Company; Column = $columnName; Before = $currentValue; After = $expectedValue })
                if (-not $DryRun) { $targetSheet.Cells.Item($targetRow, $column).Value2 = $expectedValue }
            }
        }

        if ($ExpectedChanges -ge 0 -and $changes.Count -ne $ExpectedChanges) {
            throw "La conciliacion produjo $($changes.Count) cambios; se esperaban $ExpectedChanges."
        }
        if (-not $DryRun) { $targetBook.Save() }
    }
    finally {
        if ($targetBook) { $targetBook.Close($false) }
        if ($sourceBook) { $sourceBook.Close($false) }
    }
}
finally {
    $excel.Quit()
    [Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}

[pscustomobject]@{
    DryRun = [bool]$DryRun
    Year = $Year
    Month = $Month
    Strategy = 'UPDATE_COLUMNS'
    Key = 'Ppto/Real + Ano + Mes Num + Grupo Empresa + Empresa'
    SourceSHA256 = $sourceHash
    TargetSHA256Before = $targetHash
    OutputPath = if ($DryRun) { $null } else { $OutputPath }
    OutputSHA256 = if ($DryRun) { $null } else { Get-Sha256 $OutputPath }
    ChangeCount = $changes.Count
    Changes = $changes
    AlreadyMatchingCount = $unchanged.Count
    AlreadyMatching = $unchanged
    SourceNullCount = $sourceNulls.Count
    SourceNulls = $sourceNulls
} | ConvertTo-Json -Depth 6
