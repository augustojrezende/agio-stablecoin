"""Google Trends: interesse de busca, importado de arquivos CSV exportados.

Não usamos API não oficial: ela costuma ser bloqueada e muda sem aviso.
O fluxo é manual e reproduzível:

1. Em trends.google.com, escolha Brasil, os termos ("dólar", "comprar dólar",
   "USDT") e uma janela de até 8 meses (janelas maiores viram semanais).
2. Exporte o CSV de "Interesse ao longo do tempo" para
   dados/manual/google_trends/, um arquivo por janela.
3. Faça janelas consecutivas se sobreporem em pelo menos 30 dias.

Cada janela vem normalizada de 0 a 100 dentro dela mesma. Para formar uma
série longa, `encadear` reescala cada janela pela razão média nos dias
sobrepostos com a anterior (método usual de "chaining").
"""

from __future__ import annotations

import csv
import io
from pathlib import Path

import pandas as pd


def _valor(texto: str) -> float:
    texto = texto.strip()
    if texto == "<1":
        return 0.5
    try:
        return float(texto)
    except ValueError:
        return float("nan")


def ler_csv(caminho: Path | str) -> pd.DataFrame:
    """Lê um CSV exportado do Google Trends (formatos em português ou inglês).

    Ignora as linhas de cabeçalho ("Categoria: ...") e localiza a primeira
    linha cuja primeira coluna é uma data. Devolve: data, termo, interesse.
    """
    texto = Path(caminho).read_text(encoding="utf-8-sig")
    linhas = list(csv.reader(io.StringIO(texto)))
    cabecalho, dados = None, []
    for i, linha in enumerate(linhas):
        if len(linha) < 2:
            continue
        if pd.to_datetime(linha[0], errors="coerce", format="mixed") is not pd.NaT:
            cabecalho = linhas[i - 1]
            dados = [l for l in linhas[i:] if len(l) >= 2]
            break
    if cabecalho is None:
        raise ValueError(f"Nenhuma linha de dados encontrada em {caminho}")
    termos = [c.split(":")[0].strip() for c in cabecalho[1:]]
    registros = []
    for linha in dados:
        dia = pd.to_datetime(linha[0], format="mixed").date()
        for termo, bruto in zip(termos, linha[1:]):
            registros.append({"data": dia, "termo": termo, "interesse": _valor(bruto)})
    return pd.DataFrame(registros)


def encadear(janelas: list[pd.DataFrame]) -> pd.DataFrame:
    """Une janelas sobrepostas numa série contínua por termo.

    A primeira janela é a referência; cada seguinte é multiplicada pela razão
    entre as médias da série acumulada e da janela nos dias em comum.
    """
    if not janelas:
        return pd.DataFrame(columns=["data", "termo", "interesse"])
    janelas = sorted(janelas, key=lambda j: j["data"].min())
    partes = []
    for termo in sorted(set().union(*(j["termo"] for j in janelas))):
        acumulado = None
        for janela in janelas:
            atual = janela[janela["termo"] == termo].set_index("data")["interesse"]
            if acumulado is None:
                acumulado = atual
                continue
            comum = acumulado.index.intersection(atual.index)
            base, nova = acumulado.loc[comum].mean(), atual.loc[comum].mean()
            if len(comum) == 0 or not nova or pd.isna(nova):
                raise ValueError(
                    f"Janelas sem sobreposição útil para '{termo}'; "
                    "exporte janelas que se sobreponham em pelo menos 30 dias."
                )
            atual = atual * (base / nova)
            acumulado = pd.concat([acumulado, atual[~atual.index.isin(acumulado.index)]])
        partes.append(acumulado.sort_index().rename("interesse").reset_index().assign(termo=termo))
    return pd.concat(partes, ignore_index=True)[["data", "termo", "interesse"]]


def importar_pasta(pasta: Path) -> pd.DataFrame:
    arquivos = sorted(Path(pasta).glob("*.csv"))
    if not arquivos:
        raise FileNotFoundError(f"Nenhum CSV do Google Trends em {pasta}")
    return encadear([ler_csv(a) for a in arquivos])
