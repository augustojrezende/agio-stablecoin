"""Camadas de dados: bruto (como veio da API) e tratado (tabelas padronizadas).

Regra: nada em dados/bruto é editado. Toda transformação sai de código.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2] / "dados"
BRUTO = RAIZ / "bruto"
TRATADO = RAIZ / "tratado"


def salvar_bruto(fonte: str, conteudo, rotulo: str, raiz: Path = BRUTO) -> Path:
    """Grava a resposta da API com carimbo de horário de coleta (UTC)."""
    agora = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    pasta = raiz / fonte
    pasta.mkdir(parents=True, exist_ok=True)
    caminho = pasta / f"{rotulo}_coletado-{agora}.json"
    caminho.write_text(json.dumps(conteudo, ensure_ascii=False), encoding="utf-8")
    return caminho


def atualizar_tratado(nome: str, novo: pd.DataFrame, chaves: list[str],
                      raiz: Path = TRATADO) -> pd.DataFrame:
    """Junta o novo lote ao arquivo existente; em conflito, vale a coleta mais recente."""
    raiz.mkdir(parents=True, exist_ok=True)
    caminho = raiz / f"{nome}.csv"
    if caminho.exists():
        antigo = pd.read_csv(caminho, parse_dates=["data"])
        antigo["data"] = antigo["data"].dt.date
        novo = pd.concat([antigo, novo], ignore_index=True)
    novo = novo.drop_duplicates(chaves, keep="last").sort_values(chaves)
    novo.to_csv(caminho, index=False)
    return novo.reset_index(drop=True)


def ler_tratado(nome: str, raiz: Path = TRATADO) -> pd.DataFrame:
    caminho = raiz / f"{nome}.csv"
    if not caminho.exists():
        raise FileNotFoundError(f"{caminho} não existe; rode a coleta antes.")
    df = pd.read_csv(caminho, parse_dates=["data"])
    df["data"] = df["data"].dt.date
    return df
