# Ágio da stablecoin em reais

Indicador diário do ágio do USDT negociado em reais sobre o dólar oficial (PTAX): um termômetro do estresse fiscal no Brasil (2020–2026). Código e dados abertos do TCC em Economia *O ágio da stablecoin em reais: um termômetro do estresse fiscal no Brasil (2020–2026)*.

```
ágio = fechamento do USDT/BRL na corretora / PTAX de venda − 1
```

## Fontes (todas gratuitas, sem chave)

| Fonte | Dado | Endpoint |
| --- | --- | --- |
| Banco Central (Olinda) | PTAX de fechamento | `olinda.bcb.gov.br/.../CotacaoDolarPeriodo` |
| Banco Central (SGS) | Selic diária (série 11) | `api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados` |
| Binance | Candles diários `USDTBRL` | `data-api.binance.vision/api/v3/klines` |
| Mercado Bitcoin | Candles diários `USDT-BRL` | `api.mercadobitcoin.net/api/v4/candles` |

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest                             # 6 testes, sem rede

agio coletar --inicio 2024-01-01   # baixa até hoje
agio calcular                      # gera dados/tratado/agio_*.csv
agio grafico                       # salva dados/grafico_agio.png
```

**Primeira coleta urgente:** rode `agio coletar` com o início mais antigo que as corretoras aceitarem. Os três eventos do estudo são de 2026, e as APIs nem sempre guardam histórico longo.

Depois, agende `agio coletar --inicio <ontem>` uma vez por dia (cron no Linux/Mac, Agendador de Tarefas no Windows). A coleta é idempotente: rodar de novo o mesmo período só substitui pelos dados mais recentes.

## Estrutura

```
src/agio/
  fontes/          um módulo por fonte: baixar() bruto, tratar() padronizado
  armazenamento.py camadas bruto e tratado
  indicador.py     cálculo do ágio e consolidação ponderada por volume
  cli.py           linha de comando
dados/
  bruto/           respostas das APIs como vieram, com horário da coleta (não editar)
  tratado/         ptax.csv, selic.csv, precos_usdt_brl.csv, agio_por_fonte.csv, agio_diario.csv
docs/decisoes.md   diário de decisões metodológicas
tests/
```

## Cobertura verificada

| Fonte | Primeiro dia disponível |
| --- | --- |
| Binance (`USDTBRL`) | 13/10/2020 |
| Mercado Bitcoin (`USDT-BRL`) | 11/03/2023 |

Recomendação: `agio coletar --inicio 2020-10-01`.

## Checagens antes de confiar nos dados

- Confira se o formato da resposta do Mercado Bitcoin continua o descrito em `fontes/mercadobitcoin.py`; se mudar, só o `tratar()` precisa de ajuste.
- Se a Binance bloquear sua região, use o espelho `data-api.binance.vision` (já configurado) ou desative a fonte em `cli.py`.
- Compare alguns dias da PTAX com o site do Banco Central.
- No começo de cada série há negócios isolados com preços absurdos (no Mercado Bitcoin, mínimos de R$ 0,66 por dólar em 2023). O indicador usa o fechamento, mas filtre dias de volume muito baixo.

## Licenças

- **Código:** MIT (arquivo `LICENSE`).
- **Dados derivados** em `dados/tratado/` (séries de preços consolidadas e do ágio): [Creative Commons Atribuição 4.0 (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.pt-br) (arquivo `LICENSE-DADOS.md`).
- Os dados de origem continuam sujeitos aos termos de cada fonte (Banco Central, Binance, Mercado Bitcoin).

## Como citar

Rezende, Augusto. *O ágio da stablecoin em reais: um termômetro do estresse fiscal no Brasil (2020–2026)*. Código e dados. Disponível em: https://github.com/augustojrezende/agio-stablecoin.
