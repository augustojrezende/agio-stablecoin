"""Tesouro Direto: taxas históricas dos títulos, para o juro real longo.

Fonte: Tesouro Transparente, conjunto "Taxas dos Títulos Ofertados pelo
Tesouro Direto" (CSV único com todo o histórico, cerca de 14 MB).

O termômetro de medo fiscal é o juro real de 10 anos: para cada dia, a taxa
dos títulos "Tesouro IPCA+" (sem cupom) é interpolada no prazo de 10 anos.
Usa a taxa da manhã, que coincide com a janela da PTAX.
"""

from __future__ import annotations

import io
import unicodedata

import numpy as np
import pandas as pd
import requests

from agio.http import USER_AGENT

CSV_URL = (
    "https://www.tesourotransparente.gov.br/ckan/dataset/"
    "df56aa42-484a-4a59-8184-7676580c81e3/resource/"
    "796d2059-14e9-44e3-80c9-2d9e30b405c1/download/precotaxatesourodireto.csv"
)
PRAZO_ALVO_ANOS = 10.0


def baixar() -> str:
    resp = requests.get(CSV_URL, timeout=120, headers={"User-Agent": USER_AGENT})
    resp.raise_for_status()
    resp.encoding = resp.encoding or "latin-1"
    return resp.text


def _norm(texto: str) -> str:
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return "".join(c for c in sem_acento.lower() if c.isalnum())


def _coluna(df: pd.DataFrame, *partes: str) -> str:
    for c in df.columns:
        if all(p in _norm(c) for p in partes):
            return c
    raise KeyError(f"Coluna com {partes} não encontrada: {list(df.columns)}")


def tratar(texto: str) -> pd.DataFrame:
    """data, tipo, vencimento, taxa (taxa de compra da manhã, % a.a.)."""
    df = pd.read_csv(io.StringIO(texto), sep=";", decimal=",", dtype=str)
    tipo = _coluna(df, "tipo")
    venc = _coluna(df, "vencimento")
    base = _coluna(df, "database")
    taxa = _coluna(df, "taxa", "compra", "manha")
    saida = pd.DataFrame({
        "data": pd.to_datetime(df[base], dayfirst=True, errors="coerce").dt.date,
        "tipo": df[tipo].str.strip(),
        "vencimento": pd.to_datetime(df[venc], dayfirst=True, errors="coerce").dt.date,
        "taxa": pd.to_numeric(df[taxa].str.replace(",", "."), errors="coerce"),
    })
    return saida.dropna().reset_index(drop=True)


def juro_real_10a(titulos: pd.DataFrame) -> pd.DataFrame:
    """Juro real de 10 anos por dia, interpolado entre os Tesouro IPCA+ do dia.

    Sem título dos dois lados do prazo-alvo, usa o de prazo mais próximo.
    """
    ipca = titulos[titulos["tipo"].str.fullmatch(r"Tesouro IPCA\+", case=False)
                   & (titulos["taxa"] > 0)].copy()
    ipca["prazo"] = (pd.to_datetime(ipca["vencimento"]) - pd.to_datetime(ipca["data"])).dt.days / 365.25
    linhas = []
    for dia, g in ipca.groupby("data"):
        g = g.sort_values("prazo")
        if g["prazo"].min() <= PRAZO_ALVO_ANOS <= g["prazo"].max():
            valor = float(np.interp(PRAZO_ALVO_ANOS, g["prazo"], g["taxa"]))
        else:
            valor = float(g.loc[(g["prazo"] - PRAZO_ALVO_ANOS).abs().idxmin(), "taxa"])
        linhas.append({"data": dia, "juro_real_10a": valor})
    return pd.DataFrame(linhas, columns=["data", "juro_real_10a"])
