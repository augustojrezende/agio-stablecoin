"""Regressões das correções autorizadas na AUD-002; sem consultas à rede."""
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from agio import analise, cli, episodio, relatorio
from agio.janela import preco_janela_ptax

ROOT = Path(__file__).resolve().parents[1]


def carregar_eventos():
    spec = importlib.util.spec_from_file_location('montar_eventos_aud002', ROOT / 'scripts/montar_eventos.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_aud06_multiplos_lotes_preservam_candles_e_ultima_coleta(tmp_path, monkeypatch):
    pasta = tmp_path / 'binance_1h'
    pasta.mkdir()
    def candle(h, preco):
        return [int(pd.Timestamp(f'2026-01-02 {h}:00', tz='UTC').timestamp()*1000), str(preco), str(preco+1), str(preco-1), str(preco), '2']
    (pasta/'a.json').write_text(json.dumps([candle(13, 5), candle(14, 6)]))
    (pasta/'b.json').write_text(json.dumps([candle(14, 7), candle(15, 8)]))
    monkeypatch.setattr(cli.arm, 'BRUTO', tmp_path)
    h = cli._horas_do_bruto('binance')
    assert h.index.is_unique
    assert h.inicio_utc.is_monotonic_increasing
    assert len(h) == 3 and not h.duplicated(['inicio_utc', 'fonte']).any()
    assert h.fechamento.tolist() == [5, 7, 8]
    janela = preco_janela_ptax(h, hora_fim=14)
    assert janela.volume_janela.iloc[0] == 6
    assert janela.preco_janela.iloc[0] == pytest.approx(20/3)


def test_aud06_lotes_reais_sem_perda_nem_duplicacao():
    if not any(cli.arm.BRUTO.glob('*_1h/*.json')):
        pytest.skip('requer dados/bruto (rode agio coletar-horario)')
    for fonte, (mod, _) in cli.CORRETORAS.items():
        lotes = [mod.tratar_horario(json.loads(p.read_text()), fonte)
                 for p in sorted((cli.arm.BRUTO/f'{fonte}_1h').glob('*.json'))]
        esperado = (pd.concat(lotes, ignore_index=True)
                    .drop_duplicates(['inicio_utc', 'fonte'], keep='last')
                    .sort_values(['inicio_utc', 'fonte']).reset_index(drop=True))
        observado = cli._horas_do_bruto(fonte)
        assert observado.index.is_unique
        pd.testing.assert_frame_equal(observado.reset_index(drop=True), esperado)
        assert len(preco_janela_ptax(observado, hora_fim=14)) > 0


def test_aud10_casos_reais_e_somente_duas_flags_mudam():
    if not (ROOT/'dados/tratado/ptax.csv').exists():
        pytest.skip('requer dados/tratado/ptax.csv (rode agio coletar)')
    mod = carregar_eventos()
    novo = mod.montar().astype(str)
    # A lista versionada é exatamente a que o script gera.
    pd.testing.assert_frame_equal(novo, pd.read_csv(ROOT/'dados/manual/eventos.csv').astype(str))
    # Contra a lista original (commit 543fdea), só as duas marcações mudam.
    velho = pd.read_csv(ROOT/'auditorias/AUD-002/baseline_original/dados/manual/eventos.csv').astype(str)
    pd.testing.assert_frame_equal(novo.drop(columns='sobreposto'), velho.drop(columns='sobreposto'))
    mudam = novo[novo.sobreposto != velho.sobreposto]
    assert set(zip(mudam.data, mudam.tipo)) == {('2021-10-28', 'monetario'), ('2021-11-04', 'externo')}
    assert set(mudam.sobreposto) == {'sim'}


def test_aud10_intersecao_usa_dias_observados_e_nao_sobrepoe_tipo_igual():
    mod = carregar_eventos()
    cal = pd.to_datetime(['2021-10-27','2021-10-28','2021-10-29','2021-11-01','2021-11-03','2021-11-04','2021-11-05','2021-11-08','2021-11-09','2021-11-10'])
    ev = pd.DataFrame({'data':['2021-10-28','2021-11-04','2021-11-10'], 'tipo':['monetario','externo','externo']})
    out = mod.marcar_sobreposicoes(ev, cal)
    assert out.sobreposto.tolist() == ['sim','sim','nao']
    pd.testing.assert_frame_equal(ev, out.drop(columns='sobreposto'))
    pd.testing.assert_frame_equal(out, mod.marcar_sobreposicoes(ev, cal))


def test_aud26_mediana_desenhada_igual_referencia_anormal(tmp_path, monkeypatch):
    valores = pd.Series(np.arange(80, dtype=float)**1.2)
    dados = pd.DataFrame({'data':pd.bdate_range('2024-01-01',periods=80), 'agio_pct':valores})
    monkeypatch.setattr(relatorio, '_ler', lambda p: dados if p.name=='agio_diario.csv' else None)
    guardado = []
    monkeypatch.setattr(relatorio, '_salvar', lambda fig,*args:guardado.append(fig))
    relatorio.fig_serie(relatorio._plt(), [])
    curva = guardado[0].axes[0].lines[1].get_ydata()
    referencia = valores - analise._anormal(valores)
    np.testing.assert_allclose(curva, referencia, atol=1e-14, equal_nan=True)
    assert np.isnan(curva[:30]).all()


def dados_trajetoria():
    dias = pd.bdate_range('2023-01-01',periods=120)
    v = np.sin(np.arange(120)/7)
    v[30] = np.nan
    b = pd.DataFrame({'data':dias,'y':v})
    e = pd.DataFrame({'data':[dias[30],dias[75]],'tipo':['fiscal','fiscal'],'descricao':['a','b']})
    return b,e


def test_aud27_n_efetivo_variavel_sem_mudar_media_ou_placebo():
    b,e = dados_trajetoria()
    tr = analise.trajetoria_evento(b,e,'y',antes=2,depois=2,n_sorteios=100)
    assert tr.n_eventos.tolist() == [2,2,1,2,2]
    assert tr.n_eventos_nominal.tolist() == [2]*5
    assert tr.n_placebo_sorteado.tolist() == [2]*5
    spec = importlib.util.spec_from_file_location('analise_baseline', ROOT/'auditorias/AUD-002/baseline_original/src/agio/analise.py')
    old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)
    ref = old.trajetoria_evento(b,e,'y',antes=2,depois=2,n_sorteios=100)
    for c in ['dia','media','placebo_media','placebo_p025','placebo_p975']:
        np.testing.assert_array_equal(tr[c],ref[c])


def test_aud27_grafico_publica_n_por_dia_e_tabela(tmp_path, monkeypatch):
    b,e = dados_trajetoria()
    monkeypatch.setattr(relatorio,'FIGURAS',tmp_path)
    figs=[]
    relatorio.fig_trajetorias(relatorio._plt(),figs,b,e,'y','teste.png','Título','Unidade','Legenda',tipos=('fiscal',))
    csv = tmp_path/'teste_fiscal.csv'
    assert csv.exists()
    tr = pd.read_csv(csv)
    assert tr.n_eventos.min() == 1 and tr.n_eventos.max() == 2
    assert 'n válido por dia' in figs[0][1]
    assert (tmp_path/'teste.png').exists()


def test_aud31_volume_usdt_variacao_e_texto():
    b=pd.DataFrame({'no_episodio':[False,True], 'volume_janela_binance':[100.,150.]})
    texto=episodio.resumo(b)
    assert 'volume_janela_binance (USDT)' in texto
    assert '+50.00%' in texto
    assert 'R$' not in texto
    doc=(ROOT/'docs/resultados.md').read_text()
    assert '17,1 mi → 26,1 mi de USDT' in doc
    assert 'R$ 17,1 mi → R$ 26,1 mi' not in doc
