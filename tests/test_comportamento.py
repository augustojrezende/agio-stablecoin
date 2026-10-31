"""Testes sem rede: dados de comportamento da Binance, Google Trends e painel."""

from datetime import date

import pandas as pd
import pytest

from agio.comportamento import painel_diario, sinais_mercado
from agio.fontes import binance, google_trends

DIA_MS = 1_793_664_000_000  # 2026-11-03 00:00 UTC

CSV_PT = """Categoria: Todas as categorias

Dia,dólar: (Brasil),USDT: (Brasil)
2026-10-01,40,<1
2026-10-02,50,2
2026-10-03,100,3
"""


def test_binance_mantem_dados_de_comportamento():
    bruto = [[DIA_MS, "5.40", "5.50", "5.35", "5.45", "1000", DIA_MS + 1,
              "5450", 50, "700", "3815", "0"]]
    df = binance.tratar(bruto)
    assert df.loc[0, "num_negocios"] == 50
    assert df.loc[0, "volume_compra_taker"] == 700
    assert df.loc[0, "volume_brl"] == 5450


def test_sinais_de_mercado():
    precos = pd.DataFrame({
        "data": [date(2026, 10, 26)], "fonte": ["binance"], "volume_base": [1000.0],
        "volume_brl": [5500.0], "num_negocios": [50], "volume_compra_taker": [700.0],
    })
    s = sinais_mercado(precos)
    assert s.loc[0, "pressao_compradora"] == pytest.approx(0.7)
    assert s.loc[0, "ticket_medio_brl"] == pytest.approx(110.0)


def test_sinais_sem_dados_de_comportamento_ficam_vazios():
    precos = pd.DataFrame({"data": [date(2026, 10, 26)], "fonte": ["mercadobitcoin"],
                           "volume_base": [100.0]})
    s = sinais_mercado(precos)
    assert s["pressao_compradora"].isna().all()


def test_ler_csv_google_trends(tmp_path):
    arquivo = tmp_path / "janela1.csv"
    arquivo.write_text(CSV_PT, encoding="utf-8")
    df = google_trends.ler_csv(arquivo)
    assert set(df["termo"]) == {"dólar", "USDT"}
    usdt = df[df["termo"] == "USDT"].set_index("data")["interesse"]
    assert usdt[date(2026, 10, 1)] == 0.5  # "<1" vira 0,5


def test_encadear_reescala_pela_sobreposicao():
    def janela(datas, valores):
        return pd.DataFrame({"data": datas, "termo": "dólar", "interesse": valores})

    d = [date(2026, 10, i) for i in range(1, 6)]
    a = janela(d[:3], [10.0, 20.0, 40.0])
    b = janela(d[1:], [50.0, 100.0, 80.0, 60.0])  # mesma realidade, escala 2,5x
    serie = google_trends.encadear([b, a]).set_index("data")["interesse"]
    assert serie[d[0]] == pytest.approx(10.0)
    assert serie[d[3]] == pytest.approx(32.0)
    assert serie[d[4]] == pytest.approx(24.0)


def test_encadear_sem_sobreposicao_falha():
    a = pd.DataFrame({"data": [date(2026, 1, 1)], "termo": "x", "interesse": [10.0]})
    b = pd.DataFrame({"data": [date(2026, 6, 1)], "termo": "x", "interesse": [10.0]})
    with pytest.raises(ValueError):
        google_trends.encadear([a, b])


def test_painel_diario():
    dia = pd.DataFrame({"data": [date(2026, 10, 26)], "agio": [0.01],
                        "agio_pct": [1.0], "n_fontes": [2]})
    sinais = pd.DataFrame({
        "data": [date(2026, 10, 26)] * 2, "fonte": ["binance", "mercadobitcoin"],
        "num_negocios": [50, float("nan")], "pressao_compradora": [0.7, float("nan")],
        "ticket_medio_brl": [110.0, float("nan")],
    })
    buscas = pd.DataFrame({"data": [date(2026, 10, 26)], "termo": ["comprar dólar"],
                           "interesse": [80.0]})
    p = painel_diario(dia, sinais, buscas)
    assert p.loc[0, "pressao_compradora"] == pytest.approx(0.7)
    assert p.loc[0, "busca_comprar_dólar"] == 80.0
