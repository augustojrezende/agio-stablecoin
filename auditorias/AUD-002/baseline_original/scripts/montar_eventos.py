"""Gera dados/manual/eventos.csv a partir da regra fixada em docs/decisoes.md.

Rode `python scripts/montar_eventos.py` para reproduzir a lista. Mudanças na
lista devem ser feitas aqui (e registradas no diário), nunca à mão no CSV.

Convenção de data: `data` é o primeiro dia em que a janela da PTAX (10h-13h
de Brasília) pode reagir. Anúncio depois das 13h ou fora do horário de
mercado -> dia seguinte (o teste leva ao próximo dia útil com dados).
`data_anuncio` guarda a data original.
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import pandas as pd

SAIDA = Path(__file__).resolve().parents[1] / "dados" / "manual" / "eventos.csv"
FIM_DADOS = date(2026, 10, 30)

FONTES_COPOM = {
    2020: "https://www.bcb.gov.br/controleinflacao/historicotaxasjuros",
    2021: "https://www.suno.com.br/noticias/?p=69971",
    2022: "https://www.seudinheiro.com/2021/economia/banco-central-veja-as-datas-das-reunioes-do-copom-em-2022",
    2023: "https://www.moneytimes.com.br/veja-o-calendario-de-reunioes-do-copom-para-2023/",
    2024: "https://wp.ufpel.edu.br/superavit/2023/10/13/expectativa-na-queda-dos-juros-confira-o-cronograma-do-copom-o-final-do-ano-e-2024/",
    2025: "https://clubedospoupadores.com/selic/copom",
    2026: "https://investidor10.com.br/noticias/copom-em-2026-tera-oito-reunioes-veja-o-cronograma-divulgado-pelo-bc-113749/",
}
# Segundo dia de cada reunião (decisão divulgada por volta das 18h30).
COPOM = [
    "2020-10-28", "2020-12-09",
    "2021-01-20", "2021-03-17", "2021-05-05", "2021-06-16", "2021-08-04", "2021-09-22", "2021-10-27", "2021-12-08",
    "2022-02-02", "2022-03-16", "2022-05-04", "2022-06-15", "2022-08-03", "2022-09-21", "2022-10-26", "2022-12-07",
    "2023-02-01", "2023-03-22", "2023-05-03", "2023-06-21", "2023-08-02", "2023-09-20", "2023-11-01", "2023-12-13",
    "2024-01-31", "2024-03-20", "2024-05-08", "2024-06-19", "2024-07-31", "2024-09-18", "2024-11-06", "2024-12-11",
    "2025-01-29", "2025-03-19", "2025-05-07", "2025-06-18", "2025-07-30", "2025-09-17", "2025-11-05", "2025-12-10",
    "2026-01-28", "2026-03-18", "2026-04-29", "2026-06-17", "2026-08-05", "2026-09-16",
]

FONTE_FOMC = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
FONTE_FOMC_2020 = "https://www.federalreserve.gov/monetarypolicy/fomchistorical2020.htm"
# Segundo dia de cada reunião (decisão às 14h de Nova York, depois da janela da PTAX).
FOMC = [
    "2020-11-05", "2020-12-16",
    "2021-01-27", "2021-03-17", "2021-04-28", "2021-06-16", "2021-07-28", "2021-09-22", "2021-11-03", "2021-12-15",
    "2022-01-26", "2022-03-16", "2022-05-04", "2022-06-15", "2022-07-27", "2022-09-21", "2022-11-02", "2022-12-14",
    "2023-02-01", "2023-03-22", "2023-05-03", "2023-06-14", "2023-07-26", "2023-09-20", "2023-11-01", "2023-12-13",
    "2024-01-31", "2024-03-20", "2024-05-01", "2024-06-12", "2024-07-31", "2024-09-18", "2024-11-07", "2024-12-18",
    "2025-01-29", "2025-03-19", "2025-05-07", "2025-06-18", "2025-07-30", "2025-09-17", "2025-10-29", "2025-12-10",
    "2026-01-28", "2026-03-18", "2026-04-29", "2026-06-17", "2026-07-29", "2026-09-16", "2026-10-28",
]

FONTE_ADCT = ("Prazo constitucional (ADCT, art. 35, §2º) - conferir data de envio: "
              "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm")
FONTE_RARDP = ("Prazo da LDO (22º dia após o bimestre; LRF, art. 9º) - conferir data efetiva: "
               "https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp101.htm")

# Anúncios não agendados: (data_anuncio, depois_da_janela, tipo, descrição, fonte)
NAO_AGENDADOS = [
    ("2021-10-21", False, "fiscal", "Governo propõe mudar o teto de gastos para pagar o Auxílio Brasil de R$ 400 (Guedes pede 'licença para gastar')",
     "https://www.poder360.com.br/economia/bolsa-cai-2-e-dolar-vai-a-r-568-apos-guedes-falar-em-licenca-para-gastar/"),
    ("2022-11-16", True, "fiscal", "Alckmin entrega ao Senado a minuta da PEC da Transição (Bolsa Família fora do teto)",
     "https://www12.senado.leg.br/noticias/materias/2022/11/16/alckmin-entrega-ao-senado-sugestao-de-texto-da-pec-da-transicao"),
    ("2023-03-30", False, "fiscal", "Haddad apresenta o novo arcabouço fiscal",
     "https://www.metropoles.com/brasil/politica-brasil/haddad-anuncia-novo-arcabouco-fiscal"),
    ("2024-11-27", True, "fiscal", "Pronunciamento do pacote fiscal (corte de gastos e isenção do IR até R$ 5 mil)",
     "https://www.dgabc.com.br/Noticia/4178656/haddad-anuncia-pacote-de-corte-de-r-70-bi-e-isencao-de-ir-ate-r-5-mil-dolar-dispara"),
    ("2025-05-22", True, "fiscal", "Decreto de aumento do IOF para cumprir a meta fiscal",
     "https://diariodonordeste.verdesmares.com.br/negocios/meta-fiscal-governo-federal-aumenta-iof-e-preve-arrecadacao-de-r-615-bi-em-dois-anos-1.3652854"),
    ("2024-08-05", False, "externo", "Turbulência global (desmonte de operações com iene; maior queda do Nikkei desde 1987)",
     "https://investnews.com.br/economia/indice-acionario-do-japao-nikkei-sofre-maior-queda-desde-crash-de-1987/amp/"),
    ("2024-11-05", True, "externo", "Eleição presidencial nos EUA (resultado na madrugada de 06/11)",
     "https://www.poder360.com.br/poder-economia/apos-trump-dolar-cai-para-r-568-e-bolsa-mantem-130-mil-pontos/"),
    ("2025-04-02", True, "externo", "Anúncio das tarifas recíprocas dos EUA ('Dia da Libertação'), depois do fechamento",
     "https://www.poder360.com.br/poder-economia/trump-anuncia-tarifa-reciproca-de-10-contra-o-brasil/?wldcnkw"),
    ("2025-04-09", True, "externo", "Pausa de 90 dias nas tarifas dos EUA (anunciada por volta das 14h de Brasília)",
     "https://www.ewn.co.za/2025/04/09/trump-declares-90-day-reciprocal-tariff-pause-except-for-china"),
    ("2025-07-09", True, "externo", "Carta de Trump anuncia tarifa de 50% sobre produtos brasileiros",
     "https://www.poder360.com.br/poder-internacional/trump-anuncia-tarifa-de-50-para-produtos-do-brasil/"),
    ("2026-03-16", False, "externo", "Guerra no Irã: juros futuros disparam e Tesouro faz recompra recorde de títulos",
     "https://investidor10.com.br/noticias/tesouro-recompra-r-12-bi-em-titulos-publicos-na-tentativa-de-conter-alta-dos-juros-119237/"),
]

# Eventos agendados com data fixa conhecida: (data_anuncio, depois_da_janela, tipo, descrição, fonte)
OUTROS_AGENDADOS = [
    ("2022-10-02", True, "politico", "Primeiro turno da eleição presidencial de 2022 (domingo)",
     "https://www.tse.jus.br/eleicoes/eleicoes-2022"),
    ("2022-10-30", True, "politico", "Segundo turno da eleição presidencial de 2022 (domingo)",
     "https://www.tse.jus.br/eleicoes/eleicoes-2022"),
    ("2026-10-04", True, "politico", "Primeiro turno da eleição presidencial de 2026 (domingo)",
     "https://www.oliberal.com/politica/calendario-das-eleicoes-2026-e-aprovado-pelo-tse-veja-as-datas-dos-turnos-1.1091913"),
    ("2026-10-25", True, "politico", "Segundo turno da eleição presidencial de 2026 (domingo)",
     "https://www.band.com.br/politica/eleicoes/2026/quando-e-o-segundo-turno-das-eleicoes-2026-202607211852"),
    ("2026-02-02", False, "regulatorio", "Entram em vigor as Resoluções BCB 519 e 520 (prestadoras de serviços de ativos virtuais)",
     "https://www.machadomeyer.com.br/pt/inteligencia-juridica/publicacoes-ij/bancario-seguros-e-financeiro-ij/bcb-regulamenta-o-mercado-de-ativos-virtuais-no-brasil"),
    ("2026-05-04", False, "regulatorio", "Início previsto das obrigações de informação da Resolução BCB 521",
     "https://www.machadomeyer.com.br/pt/inteligencia-juridica/publicacoes-ij/bancario-seguros-e-financeiro-ij/bcb-regulamenta-o-mercado-de-ativos-virtuais-no-brasil"),
]
REGULATORIOS_NAO_AGENDADOS = [
    ("2025-11-10", False, "regulatorio", "Banco Central publica as normas de ativos virtuais e stablecoins (Resoluções 519, 520 e 521)",
     "https://www.demarest.com.br/banco-central-regulamenta-a-prestacao-de-servicos-de-ativos-virtuais/"),
    ("2026-06-18", True, "regulatorio", "Resolução BCB 574 adia para 03/11/2026 o reporte de operações com ativos virtuais no câmbio",
     "https://www.letsmoney.com.br/noticias/bc-adia-novembro-reporte-cripto-cambio-resolucao-574/"),
]


def _d(s: str) -> date:
    return date.fromisoformat(s)


def _ultimo_util_ate(d: date) -> date:
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d


def _linha(anuncio: date, depois: bool, tipo: str, descricao: str, fonte: str, agendado: bool) -> dict:
    data = anuncio + timedelta(days=1) if depois else anuncio
    return {"data": data, "tipo": tipo, "descricao": descricao, "data_anuncio": anuncio,
            "agendado": "sim" if agendado else "nao", "fonte": fonte}


def montar() -> pd.DataFrame:
    linhas = []
    for s in COPOM:
        d = _d(s)
        linhas.append(_linha(d, True, "monetario", "Decisão do Copom", FONTES_COPOM[d.year], True))
    for s in FOMC:
        d = _d(s)
        linhas.append(_linha(d, True, "externo", "Decisão do Fed (FOMC)",
                             FONTE_FOMC_2020 if d.year == 2020 else FONTE_FOMC, True))
    for ano in range(2021, 2027):
        pldo = _ultimo_util_ate(date(ano, 4, 15))
        ploa = _ultimo_util_ate(date(ano, 8, 31))
        linhas.append(_linha(pldo, True, "fiscal", f"Envio do PLDO {ano + 1} (metas fiscais)", FONTE_ADCT, True))
        linhas.append(_linha(ploa, True, "fiscal", f"Envio do PLOA {ano + 1}", FONTE_ADCT, True))
    bimestres = [(2020, 11)] + [(a, m) for a in range(2021, 2027) for m in (3, 5, 7, 9, 11)]
    for ano, mes in bimestres:
        d = _ultimo_util_ate(date(ano, mes, 22))
        n = {3: 1, 5: 2, 7: 3, 9: 4, 11: 5}[mes]
        linhas.append(_linha(d, True, "fiscal",
                             f"Relatório de Avaliação de Receitas e Despesas Primárias, {n}º bimestre de {ano}",
                             FONTE_RARDP, True))
    for item in NAO_AGENDADOS + REGULATORIOS_NAO_AGENDADOS:
        linhas.append(_linha(_d(item[0]), *item[1:], agendado=False))
    for item in OUTROS_AGENDADOS:
        linhas.append(_linha(_d(item[0]), *item[1:], agendado=True))

    ev = pd.DataFrame(linhas)
    ev = ev[ev["data"] <= FIM_DADOS].sort_values(["data", "tipo"]).reset_index(drop=True)

    # Sobreposição: outro evento de tipo diferente a até 4 dias úteis (janelas -1 a +3 se cruzam).
    datas = pd.to_datetime(ev["data"])
    sobreposto = []
    for i, (d, t) in enumerate(zip(datas, ev["tipo"])):
        outros = ev.index[(ev["tipo"] != t)]
        dist = [abs(len(pd.bdate_range(min(d, datas[j]), max(d, datas[j]))) - 1) for j in outros
                if abs((datas[j] - d).days) <= 7]
        sobreposto.append("sim" if any(x <= 4 for x in dist) else "nao")
    ev["sobreposto"] = sobreposto
    return ev[["data", "tipo", "descricao", "data_anuncio", "agendado", "sobreposto", "fonte"]]


if __name__ == "__main__":
    ev = montar()
    ev.to_csv(SAIDA, index=False)
    print(f"{len(ev)} eventos gravados em {SAIDA}")
    print(ev.groupby(["tipo", "agendado"]).size().to_string())
    print(f"Sobrepostos a evento de outro tipo: {(ev['sobreposto'] == 'sim').sum()}")
