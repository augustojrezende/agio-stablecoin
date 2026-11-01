# Ágio da stablecoin em reais

Indicador diário do ágio do USDT negociado em reais sobre o dólar oficial (PTAX) e sua reação a choques domésticos e externos (2020–2026). Código e dados abertos do TCC em Economia *O ágio da stablecoin em reais: reação a choques domésticos e externos no Brasil (2020–2026)*.

**[Manual completo do programa](docs/manual.md)**: o que faz, conceitos, tecnologias, todos os comandos e parâmetros, arquivos gerados e métodos.

## Em poucas palavras

**Stablecoin** é um criptoativo feito para valer sempre US$ 1, um "dólar digital". O mais usado no Brasil é o **USDT** (Tether), comprado em corretoras de criptoativos, com Pix, 24 horas por dia.

**Ágio** é quanto o USDT está mais caro (ou, no deságio, mais barato) que o dólar oficial do Banco Central (PTAX), em porcentagem. Se a PTAX é R$ 5,00 e o USDT sai por R$ 5,05, o ágio é de 1%. O ágio mostra a procura por dólar fora do câmbio oficial; o programa mede esse ágio todos os dias e testa a que tipo de notícia ele reage.

```
ágio = preço do USDT/BRL na janela da PTAX (10h às 13h de Brasília) / PTAX de venda − 1
```

A medida usa o preço do USDT no mesmo horário em que a PTAX é formada, para comparar preços do mesmo momento. Explicação completa, com exemplos, no [manual](docs/manual.md#o-que-é-ágio).

## Principais resultados (out/2020 a out/2026)

- Quando o dólar oficial sobe 1%, o ágio cai cerca de 0,13 ponto percentual no dia e continua caindo por dois dias: o USDT acompanha o câmbio oficial só em parte.
- O medo global (VIX) eleva o ágio, com resultado robusto em 7 de 9 especificações.
- O estresse fiscal doméstico (juro real de 10 anos) quase não mexe no ágio, e os anúncios fiscais não o afetam mais que dias quaisquer.

Detalhes, figuras e todas as verificações em [`docs/resultados.md`](docs/resultados.md). Os resultados novos serão confirmados com dados futuros, conforme o [pré-registro](docs/pre-registro.md).

## Começo rápido

```bash
git clone https://github.com/augustojrezende/agio-stablecoin.git
cd agio-stablecoin
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest                             # 41 testes, sem rede

agio coletar --inicio 2020-10-01   # preços diários, PTAX e Selic
agio coletar-horario --inicio 2020-10-01
agio coletar-controles             # juro real e VIX
agio calcular                      # ágio e painel diário
agio testar                        # teste formal
agio robustez                      # 9 especificações
agio relatorio                     # gráficos e tabelas
```

## Comandos

| Comando | O que faz |
| --- | --- |
| `coletar`, `coletar-horario` | Preços do USDT/BRL (diários e horários), PTAX e Selic |
| `coletar-controles` | Juro real de 10 anos e VIX |
| `importar-trends` | Buscas do Google Trends (CSVs exportados à mão) |
| `calcular`, `grafico` | Ágio, sinais de comportamento, painel diário e gráfico rápido |
| `testar` | Regressões, estudo de evento e quadro de hipóteses; com `--inicio`/`--fim`, validação fora da amostra |
| `robustez` | A regressão em 9 especificações alternativas |
| `buscas`, `oferta-usdt`, `episodio` | Análises exploratórias e diagnóstico de períodos atípicos |
| `relatorio` | Gráficos e tabelas do trabalho |

Todos os parâmetros, com exemplos, estão no [manual](docs/manual.md#comandos-e-parâmetros).

## Fontes (todas gratuitas, sem chave)

Banco Central (PTAX e Selic), Binance e Mercado Bitcoin (USDT/BRL), Tesouro Transparente (juro real), Cboe/FRED (VIX), Google Trends (buscas) e DefiLlama (oferta de USDT). Endereços e cobertura no [manual](docs/manual.md#fontes-de-dados).

## Documentação

| Arquivo | Conteúdo |
| --- | --- |
| [`docs/manual.md`](docs/manual.md) | Manual do programa |
| [`docs/resultados.md`](docs/resultados.md) | Todos os testes e verificações, na ordem em que foram feitos |
| [`docs/resultados_tabelas.md`](docs/resultados_tabelas.md) e `docs/figuras/` | Tabelas e gráficos, gerados por `agio relatorio` |
| [`docs/pre-registro.md`](docs/pre-registro.md) | Hipóteses e regras da validação com dados a partir de 02/11/2026 |
| [`docs/decisoes.md`](docs/decisoes.md) | Diário de decisões metodológicas |

## Licenças

- **Código:** MIT (arquivo `LICENSE`).
- **Dados derivados** em `dados/tratado/` (séries de preços consolidadas e do ágio): [Creative Commons Atribuição 4.0 (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.pt-br) (arquivo `LICENSE-DADOS.md`).
- Os dados de origem continuam sujeitos aos termos de cada fonte.

## Como citar

REZENDE, Augusto. *agio-stablecoin*: código e dados do ágio da stablecoin em reais. GitHub, 2026. Disponível em: https://github.com/augustojrezende/agio-stablecoin.
