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


def encadear(janelas: list[pd.DataFrame], minimo_dias_validos: int = 15) -> pd.DataFrame:
    """Une janelas sobrepostas numa série contínua por termo.

    A primeira janela de cada termo é a referência; cada seguinte é
    multiplicada pela razão entre as médias da série acumulada e da janela
    nos dias em comum. Janelas que não contêm o termo são ignoradas (termos
    exportados em arquivos separados).

    Um termo cuja sobreposição tenha menos de `minimo_dias_validos` dias com
    busca nos dois lados não pode ser encadeado com segurança (quase tudo
    zero): fica de fora, com aviso.
    """
    if not janelas:
        return pd.DataFrame(columns=["data", "termo", "interesse"])
    janelas = sorted(janelas, key=lambda j: j["data"].min())
    partes = []
    for termo in sorted(set().union(*(j["termo"] for j in janelas))):
        do_termo = [j[j["termo"] == termo] for j in janelas if (j["termo"] == termo).any()]
        acumulado, descartar = None, False
        for janela in do_termo:
            atual = janela.set_index("data")["interesse"]
            if acumulado is None:
                acumulado = atual
                continue
            comum = acumulado.index.intersection(atual.index)
            if len(comum) == 0:
                raise ValueError(
                    f"Janelas sem sobreposição para '{termo}' perto de {atual.index.min()}; "
                    "exporte janelas que se sobreponham em pelo menos 30 dias."
                )
            validos = comum[(acumulado.loc[comum] > 0.5) & (atual.loc[comum] > 0.5)]
            if len(validos) < minimo_dias_validos:
                print(f"Aviso: '{termo}' tem só {len(validos)} dias com busca na sobreposição "
                      f"perto de {atual.index.min()}; termo fora da série (volume baixo demais).")
                descartar = True
                break
            atual = atual * (acumulado.loc[validos].mean() / atual.loc[validos].mean())
            acumulado = pd.concat([acumulado, atual[~atual.index.isin(acumulado.index)]])
        if not descartar:
            partes.append(acumulado.sort_index().rename("interesse").reset_index().assign(termo=termo))
    if not partes:
        return pd.DataFrame(columns=["data", "termo", "interesse"])
    return pd.concat(partes, ignore_index=True)[["data", "termo", "interesse"]]


def importar_pasta(pasta: Path) -> pd.DataFrame:
    arquivos = sorted(Path(pasta).glob("*.csv"))
    if not arquivos:
        raise FileNotFoundError(f"Nenhum CSV do Google Trends em {pasta}")
    return encadear([ler_csv(a) for a in arquivos])
