"""Contrato estático del selector PBIP-008; no sustituye la prueba en Desktop."""

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DEFINITION = ROOT / 'PBIP/Proyecto.SemanticModel/definition'
PAGE = ROOT / 'PBIP/Proyecto.Report/definition/pages/b7f3a91c2d4e60582a1f'
TABLE = 'PBIP008 Selector Indicador'


def visual(name):
    return json.loads((PAGE / 'visuals' / name / 'visual.json').read_text(encoding='utf-8-sig'))


def measure(name):
    text = (DEFINITION / 'tables/Tbl_Medidas.tmdl').read_text(encoding='utf-8-sig')
    found = re.search(r"\tmeasure '" + re.escape(name) + r"' =([\s\S]*?)(?=\n\t(?:measure |///)|\Z)", text)
    assert found, name
    return found.group(1)


def projections(name, role):
    return visual(name)['visual']['query']['queryState'][role]['projections']


def test_selector_table_registered_and_disconnected():
    text = (DEFINITION / f'tables/{TABLE}.tmdl').read_text(encoding='utf-8-sig')
    assert '{"Retiros", "RETIROS"}, {"Rotación", "ROTACION"}' in text
    assert text.count('column ') == 2
    assert TABLE not in (DEFINITION / 'relationships.tmdl').read_text(encoding='utf-8-sig')
    assert (DEFINITION / 'model.tmdl').read_text(encoding='utf-8-sig').count(f"ref table '{TABLE}'") == 1
    assert 'SELECTEDVALUE' in measure('PBIP008 Indicador Seleccionado')
    assert '"RETIROS"' in measure('PBIP008 Indicador Seleccionado')


@pytest.mark.parametrize('suffix', [
    'Real', 'Forecast', 'Baseline', 'Referencia', 'Banda Inferior', 'Banda Superior',
    'Ultimo Cierre', 'Referencia Sintesis', 'Variacion Mensual', 'Clasificacion',
    'Metodologia', 'Estado', 'Titulo Grafico', 'Titulo Cierre', 'Titulo Exposicion',
])
def test_dynamic_measures_use_central_selection(suffix):
    dax = measure('PBIP008 Dinamico ' + suffix)
    assert '[PBIP008 Indicador Seleccionado]' in dax
    assert '"RETIROS"' in dax and '"ROTACION"' in dax
    assert 'SELECTEDVALUE' not in dax


def test_single_selection_and_persisted_default():
    v = visual('r2ind16')['visual']
    assert v['visualType'] == 'advancedSlicerVisual'
    assert projections('r2ind16', 'Values')[0]['field']['Column']['Property'] == 'Indicador'
    props = v['objects']['selection'][0]['properties']
    assert props['singleSelect']['expr']['Literal']['Value'] == 'true'
    assert props['strictSingleSelect']['expr']['Literal']['Value'] == 'true'
    assert props['selectAllCheckboxEnabled']['expr']['Literal']['Value'] == 'false'
    condition = v['objects']['general'][0]['properties']['filter']['filter']['Where'][0]['Condition']
    assert condition['In']['Values'] == [[{'Literal': {'Value': "'Retiros'"}}]]
    layout = v['objects']['layout'][0]['properties']
    assert layout['rowCount']['expr']['Literal']['Value'] == '1L'
    assert layout['columnCount']['expr']['Literal']['Value'] == '2L'


def test_chart_and_kpis_use_dynamic_measures():
    assert [p['field']['Measure']['Property'] for p in projections('r2lin08', 'Y')] == [
        'PBIP008 Dinamico ' + n for n in ['Real', 'Forecast', 'Baseline', 'Referencia', 'Banda Inferior', 'Banda Superior']
    ]
    assert [p['field']['Measure']['Property'] for p in projections('r2kpi07', 'Data')] == [
        'PBIP008 Dinamico ' + n for n in ['Ultimo Cierre', 'Variacion Mensual', 'Referencia Sintesis', 'Clasificacion']
    ]
    assert projections('r2exp09', 'Y')[0]['field']['Measure']['Property'] == 'PBIP008 Dinamico Ultimo Cierre'
    for name, role in [('r2lin08', 'Y'), ('r2kpi07', 'Data'), ('r2exp09', 'Y')]:
        for p in projections(name, role):
            assert p['queryRef'] == 'Tbl_Medidas.' + p['field']['Measure']['Property']


def test_bands_and_descriptive_labels():
    labels = visual('r2lin08')['visual']['objects']['labels']
    by_measure = {item.get('selector', {}).get('metadata'): item['properties'] for item in labels}
    for suffix in ['Inferior', 'Superior']:
        props = by_measure['Tbl_Medidas.PBIP008 Dinamico Banda ' + suffix]
        assert props['show']['expr']['Literal']['Value'] == 'true'
        assert props['fontSize']['expr']['Literal']['Value'] == '8D'
        assert props['labelPrecision']['expr']['Literal']['Value'] == '1L'
        assert props['valueCustomFormatString']['expr']['Literal']['Value'] == "'0.0 %'"
        assert props['color']['solid']['color']['expr']['Literal']['Value'] == "'#B9C4D6'"
    assert by_measure['Tbl_Medidas.PBIP008 Dinamico Referencia']['show']['expr']['Literal']['Value'] == 'false'


def test_year_and_group_fields_and_blank_exclusion():
    year = projections('r2anio15', 'Values')[0]['field']['Column']
    assert year == {'Expression': {'SourceRef': {'Entity': 'DimPeriodoYM'}}, 'Property': 'Año'}
    year_visual = visual('r2anio15')['visual']
    persisted = year_visual['objects']['general'][0]['properties']['filter']['filter']
    assert persisted['Where'][0]['Condition']['In']['Values'] == [[{'Literal': {'Value': "'2026'"}}]]
    # DimPeriodoYM inherits its year from the text column Años[Año].
    assert 'dataType: string' in (DEFINITION / 'tables/Años.tmdl').read_text(encoding='utf-8-sig')
    group = projections('r2slc14', 'Values')[0]['field']['Column']
    assert group['Property'] == 'Grupo Empresarial'
    condition = visual('r2slc14')['filterConfig']['filters'][0]['filter']['Where'][0]['Condition']
    assert condition['Not']['Expression']['In']['Values'] == [[{'Literal': {'Value': 'null'}}]]
    for suffix in ['Real', 'Forecast', 'Baseline', 'Referencia', 'Banda Inferior', 'Banda Superior']:
        assert 'REMOVEFILTERS' not in measure('PBIP008 Dinamico ' + suffix)


def test_dynamic_titles_textboxes_and_pp():
    for name, title in [('r2lin08', 'Grafico'), ('r2exp09', 'Exposicion')]:
        expr = visual(name)['visual']['visualContainerObjects']['title'][0]['properties']['text']['expr']
        assert expr['Measure']['Property'] == 'PBIP008 Dinamico Titulo ' + title
    for name, suffix in [('r2met11', 'Metodologia'), ('r2msg06', 'Estado')]:
        objects = visual(name)['visual']['objects']
        assert 'PBIP008 Dinamico ' + suffix in json.dumps(objects['values'])
        assert any(isinstance(run['value'], dict) for p in objects['general'][0]['properties']['paragraphs'] for run in p['textRuns'])
    dax = measure('PBIP008 Dinamico Variacion Mensual')
    assert '100 * SWITCH' in dax and '" pp"' in dax


def test_navigation_destinations_and_fixed_cutoff():
    assert 'ReportSection6a1196bf8c963b709405' in json.dumps(visual('r2nav03'))
    assert 'ReportSectiondc346876696ee4cba0ab' in json.dumps(visual('r2nav04'))
    text = json.dumps(visual('r2cor05'), ensure_ascii=False)
    assert '31/07/2026' in text and 'agosto - diciembre 2026' in text
