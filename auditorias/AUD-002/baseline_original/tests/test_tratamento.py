"""Testes sem rede: formato das respostas e cálculo do ágio."""

from datetime import date

import pandas as pd
import pytest

from agio import armazenamento as arm
from agio.fontes import bcb, binance, mercadobitcoin
from agio.indicador import calcular_agio, consolidar

DIA_MS = 1_793_664_000_000  # 2026-11-03 00:00 UTC


def test_ptax_fica_com_ultimo_boletim_do_dia():
    bruto = [
        {"cotacaoCompra": 5.30, "cotacaoVenda": 5.31, "dataHoraCotacao": "2026-10-27 10:00:00.0"},
        {"cotacaoCompra": 5.40, "cotacaoVenda": 5.41, "dataHoraCotacao": "2026-10-27 13:07:00.0"},
    ]
    df = bcb.tratar_ptax(bruto)
    assert len(df) == 1
    assert df.loc[0, "ptax_venda"] == 5.41


def test_sgs():
    df = bcb.tratar_sgs([{"data": "27/10/2026", "valor": "0.055131"}], "selic")
    assert df.loc[0, "data"] == date(2026, 10, 27)
    assert df.loc[0, "selic"] == pytest.approx(0.055131)


def test_binance():
    bruto = [[DIA_MS, "5.40", "5.50", "5.35", "5.45", "1000", DIA_MS + 1, "0", 1, "0", "0", "0"]]
    df = binance.tratar(bruto)
    assert df.loc[0, "data"] == date(2026, 11, 3)
    assert df.loc[0, "fechamento"] == 5.45
    assert df.loc[0, "fonte"] == "binance"


def test_mercadobitcoin():
    t = DIA_MS // 1000
    bruto = [{"t": [t], "o": ["5.40"], "h": ["5.50"], "l": ["5.35"], "c": ["5.47"], "v": ["200"]}]
    df = mercadobitcoin.tratar(bruto)
    assert df.loc[0, "data"] == date(2026, 11, 3)
    assert df.loc[0, "fechamento"] == 5.47


def test_agio_e_consolidacao():
    precos = pd.DataFrame({
        "data": [date(2026, 10, 26)] * 2 + [date(2026, 10, 25)],  # 25 é domingo
        "fonte": ["binance", "mercadobitcoin", "binance"],
        "fechamento": [5.50, 5.61, 5.40],
        "volume_base": [300, 100, 50],
    })
    ptax = pd.DataFrame({"data": [date(2026, 10, 26)], "ptax_venda": [5.50]})
    agio = calcular_agio(precos, ptax)
    assert len(agio) == 2  # domingo fica de fora
    assert agio.set_index("fonte").loc["mercadobitcoin", "agio_pct"] == pytest.approx(2.0)
    dia = consolidar(agio)
    # ponderado por volume: (0 * 300 + 0.02 * 100) / 400 = 0.005
    assert dia.loc[0, "agio"] == pytest.approx(0.005)


def test_tratado_mantem_coleta_mais_recente(tmp_path):
    a = pd.DataFrame({"data": [date(2026, 10, 26)], "ptax_venda": [5.0]})
    b = pd.DataFrame({"data": [date(2026, 10, 26), date(2026, 10, 27)], "ptax_venda": [5.1, 5.2]})
    arm.atualizar_tratado("ptax", a, ["data"], raiz=tmp_path)
    df = arm.atualizar_tratado("ptax", b, ["data"], raiz=tmp_path)
    assert list(df["ptax_venda"]) == [5.1, 5.2]
