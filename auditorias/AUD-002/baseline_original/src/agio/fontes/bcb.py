"""Banco Central do Brasil: PTAX (Olinda) e Selic (SGS)."""

from __future__ import annotations

from datetime import date

import pandas as pd

from agio.http import get_json

PTAX_URL = (
    "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
    "CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
)
SGS_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
SELIC_DIARIA = 11  # taxa Selic diária (% ao dia)


def baixar_ptax(inicio: date, fim: date) -> list[dict]:
    """Resposta bruta da PTAX de fechamento (compra e venda) no período."""
    params = {
        "@dataInicial": f"'{inicio:%m-%d-%Y}'",
        "@dataFinalCotacao": f"'{fim:%m-%d-%Y}'",
        "$format": "json",
    }
    return get_json(PTAX_URL, params).get("value", [])


def tratar_ptax(bruto: list[dict]) -> pd.DataFrame:
    """Uma linha por dia útil: data, ptax_compra, ptax_venda."""
    if not bruto:
        return pd.DataFrame(columns=["data", "ptax_compra", "ptax_venda"])
    df = pd.DataFrame(bruto)
    df["data"] = pd.to_datetime(df["dataHoraCotacao"]).dt.date
    df = df.rename(columns={"cotacaoCompra": "ptax_compra", "cotacaoVenda": "ptax_venda"})
    # Se houver mais de um boletim no dia, fica o último (fechamento).
    df = df.sort_values("dataHoraCotacao").drop_duplicates("data", keep="last")
    return df[["data", "ptax_compra", "ptax_venda"]].reset_index(drop=True)


def baixar_sgs(codigo: int, inicio: date, fim: date) -> list[dict]:
    """Série do SGS. Para séries diárias, a API limita a consulta a 10 anos."""
    params = {
        "formato": "json",
        "dataInicial": f"{inicio:%d/%m/%Y}",
        "dataFinal": f"{fim:%d/%m/%Y}",
    }
    return get_json(SGS_URL.format(codigo=codigo), params)


def tratar_sgs(bruto: list[dict], nome: str) -> pd.DataFrame:
    if not bruto:
        return pd.DataFrame(columns=["data", nome])
    df = pd.DataFrame(bruto)
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y").dt.date
    df[nome] = pd.to_numeric(df["valor"], errors="coerce")
    return df[["data", nome]]
