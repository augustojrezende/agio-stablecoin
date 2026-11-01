# Ágio da stablecoin em reais

Indicador diário do ágio do USDT negociado em reais sobre o dólar oficial (PTAX): um termômetro do estresse fiscal no Brasil (2020–2026). Código e dados abertos do TCC em Economia *O ágio da stablecoin em reais: um termômetro do estresse fiscal no Brasil (2020–2026)*.

```
ágio = preço do USDT/BRL na janela da PTAX (10h às 13h de Brasília) / PTAX de venda − 1
```

A PTAX é formada entre 10h e 13h; o candle diário das corretoras fecha às 21h. Em dias de crise o câmbio muda muito nesse intervalo, então a medida principal usa o preço médio do USDT, ponderado pelo volume, **na mesma janela da PTAX**. O ágio de fechamento (21h) continua sendo calculado para comparação.

## Fontes (todas gratuitas, sem chave)

| Fonte | Dado | Endpoint |
| --- | --- | --- |
| Banco Central (Olinda) | PTAX de fechamento | `olinda.bcb.gov.br/.../CotacaoDolarPeriodo` |
| Banco Central (SGS) | Selic diária (série 11) | `api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados` |
| Binance | Candles diários `USDTBRL` | `data-api.binance.vision/api/v3/klines` |
| Mercado Bitcoin | Candles diários `USDT-BRL` | `api.mercadobitcoin.net/api/v4/candles` |
| Google Trends | Interesse de busca ("dólar", "comprar dólar", "USDT") | CSV exportado manualmente de trends.google.com |

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest                             # 17 testes, sem rede

agio coletar --inicio 2020-10-01          # diário: PTAX, Selic, preços, comportamento
agio coletar-horario --inicio 2020-10-01  # horário: preço na janela da PTAX
agio calcular                      # gera dados/tratado/agio_*.csv
agio grafico                       # salva dados/grafico_agio.png
agio importar-trends               # opcional: lê os CSVs do Google Trends
```

**Primeira coleta urgente:** rode `agio coletar` desde outubro de 2020. As APIs das corretoras nem sempre guardam histórico longo.

Depois, agende `agio coletar --inicio <ontem>` uma vez por dia (cron no Linux/Mac, Agendador de Tarefas no Windows). A coleta é idempotente: rodar de novo o mesmo período só substitui pelos dados mais recentes.

## Sinais de comportamento coletivo

`agio calcular` também gera:

- `sinais_comportamento.csv`: por dia e corretora, **pressão compradora** (parcela do volume comprada por quem aceitou o preço pedido; acima de 0,5 indica pressa em comprar), **número de negócios** e **ticket médio em reais** (quanto menor, maior o peso do varejo). Hoje só a Binance informa esses dados.
- `painel_diario.csv`: ágio consolidado, sinais de mercado e buscas do Google Trends, um dia por linha.

**Google Trends, passo a passo.** Não há API oficial estável, então a importação é por CSV:

1. Em trends.google.com, escolha **Brasil**, os termos e uma janela de **até 8 meses** (janelas maiores viram dados semanais).
2. Exporte "Interesse ao longo do tempo" para `dados/manual/google_trends/`, um arquivo por janela.
3. Faça janelas consecutivas se sobreporem em **pelo menos 30 dias**: o código usa a sobreposição para colocar todas na mesma escala.
4. Rode `agio importar-trends` e depois `agio calcular`.

Os dados são agregados: medem comportamento coletivo, não a motivação de cada investidor.

## Estrutura

```
src/agio/
  fontes/          um módulo por fonte: baixar() bruto, tratar() padronizado
  armazenamento.py camadas bruto e tratado
  indicador.py     cálculo do ágio e consolidação ponderada por volume
  janela.py        preço do USDT na janela da PTAX (10h às 13h de Brasília)
  comportamento.py sinais de comportamento coletivo e painel diário
  cli.py           linha de comando
dados/
  bruto/           respostas das APIs como vieram, com horário da coleta (não editar)
  tratado/         ptax.csv, selic.csv, precos_usdt_brl.csv, precos_janela_ptax.csv,
                   agio_por_fonte.csv, agio_diario.csv (medida principal),
                   agio_fechamento_por_fonte.csv, agio_fechamento_diario.csv (comparação),
                   sinais_comportamento.csv, google_trends.csv, painel_diario.csv
  manual/          CSVs exportados do Google Trends (originais, não editar)
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
