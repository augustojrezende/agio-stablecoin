"""VIX (índice de volatilidade, termômetro do medo global), sem chave de acesso.

Fonte principal: FRED (Fed de St. Louis), série VIXCLS. O servidor às vezes
demora ou recusa conexões; nesse caso, usa o histórico oficial da Cboe, a
bolsa que calcula o índice.

O VIX é o valor de fechamento em Nova York, que sai depois da janela da PTAX;
por isso a regressão usa também a variação do dia anterior.
"""

from __future__ import annotations

import io
import time

import pandas as pd
import requests

from agio.http import USER_AGENT

CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"
CBOE_URL = "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv"


def _get(url: str, params: dict | None = None, tentativas: int = 3, timeout: int = 120) -> str:
    erro = None
    for i in range(tentativas):
        try:
            resp = requests.get(url, params=params, timeout=timeout,
                                headers={"User-Agent": USER_AGENT})
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as e:
            erro = e
            time.sleep(5 * (i + 1))
    raise RuntimeError(f"Falha ao acessar {url}: {erro}")


def baixar(serie: str = "VIXCLS") -> str:
    return _get(CSV_URL, params={"id": serie})


def tratar(texto: str, nome: str = "vix") -> pd.DataFrame:
    """Formato do FRED: aceita os cabeçalhos DATE ou observation_date."""
    df = pd.read_csv(io.StringIO(texto))
    saida = pd.DataFrame({
        "data": pd.to_datetime(df.iloc[:, 0], errors="coerce").dt.date,
        nome: pd.to_numeric(df.iloc[:, 1], errors="coerce"),  # "." vira vazio
    })
    return saida.dropna().reset_index(drop=True)


def tratar_cboe(texto: str, nome: str = "vix") -> pd.DataFrame:
    """Formato da Cboe: DATE (MM/DD/YYYY), OPEN, HIGH, LOW, CLOSE."""
    df = pd.read_csv(io.StringIO(texto))
    df.columns = [c.strip().upper() for c in df.columns]
    saida = pd.DataFrame({
        "data": pd.to_datetime(df["DATE"], format="%m/%d/%Y", errors="coerce").dt.date,
        nome: pd.to_numeric(df["CLOSE"], errors="coerce"),
    })
    return saida.dropna().reset_index(drop=True)


def baixar_vix() -> tuple[str, str, pd.DataFrame]:
    """Tenta o FRED e, se falhar, a Cboe. Devolve (fonte, texto bruto, tabela)."""
    try:
        texto = baixar("VIXCLS")
        return "fred", texto, tratar(texto)
    except RuntimeError as erro:
        print(f"FRED indisponível ({erro}); usando o histórico da Cboe.")
    texto = _get(CBOE_URL)
    return "cboe", texto, tratar_cboe(texto)
