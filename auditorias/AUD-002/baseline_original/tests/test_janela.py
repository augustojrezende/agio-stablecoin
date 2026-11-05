"""Testes sem rede: candles horários e ágio na janela da PTAX."""

from datetime import date

import pandas as pd
import pytest

from agio.fontes import binance, mercadobitcoin
from agio.indicador import calcular_agio
from agio.janela import preco_janela_ptax

H = 3_600_000
DIA_UTC_MS = 1_793_664_000_000  # 2026-11-03 00:00 UTC = 02/11 21h em Brasília


def _kline(hora_utc, preco, volume):
    t = DIA_UTC_MS + hora_utc * H
    p = str(preco)
    return [t, p, p, p, p, str(volume), t + H - 1, "0", 1, "0", "0", "0"]


def test_janela_usa_so_10h_a_13h_de_brasilia():
    # 13h, 14h e 15h UTC = 10h, 11h e 12h em Brasília (dentro da janela).
    # 12h UTC (9h) e 16h UTC (13h) ficam de fora.
    bruto = [_kline(12, 9.0, 1000), _kline(13, 5.0, 100), _kline(14, 5.2, 100),
             _kline(15, 5.6, 200), _kline(16, 9.0, 1000)]
    horas = binance.tratar_horario(bruto)
    j = preco_janela_ptax(horas)
    assert len(j) == 1
    assert j.loc[0, "data"] == date(2026, 11, 3)
    assert j.loc[0, "horas_janela"] == 3
    # média ponderada: (5.0*100 + 5.2*100 + 5.6*200) / 400 = 5.35
    assert j.loc[0, "preco_janela"] == pytest.approx(5.35)


def test_janela_sem_volume_usa_media_simples():
    bruto = [_kline(13, 5.0, 0), _kline(14, 5.4, 0)]
    j = preco_janela_ptax(binance.tratar_horario(bruto))
    assert j.loc[0, "preco_janela"] == pytest.approx(5.2)


def test_mercadobitcoin_horario():
    t0 = DIA_UTC_MS // 1000 + 13 * 3600
    bruto = [{"t": [t0, t0 + 3600], "o": ["5", "5"], "h": ["5.1", "5.3"],
              "l": ["4.9", "5.1"], "c": ["5.0", "5.2"], "v": ["10", "10"]}]
    horas = mercadobitcoin.tratar_horario(bruto)
    assert len(horas) == 2
    j = preco_janela_ptax(horas)
    assert j.loc[0, "preco_janela"] == pytest.approx(5.1)


def test_agio_alinhado_corrige_dia_de_crise():
    # Dólar disparou de manhã (PTAX 5.80) e voltou à tarde.
    # Fechamento às 21h (5.55) sugere ágio negativo; na janela (5.85), positivo.
    ptax = pd.DataFrame({"data": [date(2026, 10, 26)], "ptax_venda": [5.80]})
    fech = pd.DataFrame({"data": [date(2026, 10, 26)], "fonte": ["binance"],
                         "fechamento": [5.55], "volume_base": [1000.0]})
    jan = pd.DataFrame({"data": [date(2026, 10, 26)], "fonte": ["binance"],
                        "preco_janela": [5.85], "volume_janela": [300.0]})
    a_fech = calcular_agio(fech, ptax)
    a_jan = calcular_agio(jan, ptax, coluna_preco="preco_janela", coluna_volume="volume_janela")
    assert a_fech.loc[0, "agio_pct"] < 0
    assert a_jan.loc[0, "agio_pct"] == pytest.approx(5.85 / 5.80 * 100 - 100)
    assert a_jan.loc[0, "volume_base"] == 300.0


def test_janela_ate_14h_inclui_a_hora_das_13h():
    bruto = [_kline(13, 5.0, 100), _kline(16, 6.0, 100)]
    horas = binance.tratar_horario(bruto)
    assert preco_janela_ptax(horas).loc[0, "horas_janela"] == 1
    j = preco_janela_ptax(horas, hora_fim=14)
    assert j.loc[0, "horas_janela"] == 2
    assert j.loc[0, "preco_janela"] == pytest.approx(5.5)
