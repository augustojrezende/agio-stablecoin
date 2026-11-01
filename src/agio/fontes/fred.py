"""FRED (Fed de St. Louis): séries de controle externo, sem chave de acesso.

VIXCLS: índice de volatilidade (VIX), termômetro do medo global. É o valor de
fechamento em Nova York, que sai depois da janela da PTAX; por isso a
regressão usa também a variação do dia anterior.
"""

from __future__ import annotations

import io

import pandas as pd
import requests

from agio.http import USER_AGENT

CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"


def baixar(serie: str = "VIXCLS") -> str:
    resp = requests.get(CSV_URL, params={"id": serie}, timeout=60,
                        headers={"User-Agent": USER_AGENT})
    resp.raise_for_status()
    return resp.text


def tratar(texto: str, nome: str = "vix") -> pd.DataFrame:
    """Aceita os dois formatos de cabeçalho do FRED (DATE ou observation_date)."""
    df = pd.read_csv(io.StringIO(texto))
    col_data = df.columns[0]
    saida = pd.DataFrame({
        "data": pd.to_datetime(df[col_data], errors="coerce").dt.date,
        nome: pd.to_numeric(df.iloc[:, 1], errors="coerce"),  # "." vira vazio
    })
    return saida.dropna().reset_index(drop=True)
