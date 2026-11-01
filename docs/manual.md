# Manual do programa agio-stablecoin

*Versão de 01/11/2026 · Augusto Rezende*

## Sumário

1. [Visão geral](#visão-geral)
2. [O que é stablecoin](#o-que-é-stablecoin)
3. [O que é ágio](#o-que-é-ágio)
4. [Como funciona](#como-funciona)
5. [Tecnologias](#tecnologias)
6. [Fontes de dados](#fontes-de-dados)
7. [Instalação](#instalação)
8. [Comandos e parâmetros](#comandos-e-parâmetros)
9. [Uso típico](#uso-típico)
10. [Arquivos gerados](#arquivos-gerados)
11. [Métodos implementados](#métodos-implementados)
12. [Qualidade, reprodutibilidade e licenças](#qualidade-reprodutibilidade-e-licenças)
13. [Limitações e próximos passos](#limitações-e-próximos-passos)
14. [Como citar](#como-citar)

## Visão geral

O **agio-stablecoin** é um programa em Python, de linha de comando, que constrói um indicador diário do ágio do dólar digital (USDT) negociado em reais sobre o dólar oficial (PTAX) e testa como esse ágio reage a choques domésticos e externos. É a base empírica do TCC "O ágio da stablecoin em reais: reação a choques domésticos e externos no Brasil (2020–2026)".

**O que faz:**

- Coleta, de fontes públicas e gratuitas, os preços do USDT/BRL, a PTAX, o juro real de 10 anos, o VIX, buscas no Google e a oferta global de USDT.
- Calcula o ágio diário no mesmo horário da PTAX (10h às 13h), por corretora e consolidado.
- Roda os testes do trabalho: regressões, estudo de evento com teste de permutação, robustez em 9 especificações e o quadro de hipóteses pré-registradas.
- Gera os gráficos e as tabelas do trabalho.

**Para que serve:**

- Medir, com dados diários desde outubro de 2020, um canal novo de procura por dólar que as estatísticas oficiais captam mal.
- Permitir que qualquer pesquisador reproduza todos os resultados do TCC com poucos comandos e continue a série com dados novos.
- Servir de base para artigos e para o mestrado (validação fora da amostra até 2028).

**Em números:** 1.520 dias úteis analisados (13/10/2020 a 30/10/2026), 7 fontes de dados, 12 comandos, 158 eventos com fonte, 41 testes automatizados.

## O que é stablecoin

**Stablecoin** ("moeda estável") é um criptoativo feito para valer sempre o mesmo que uma moeda tradicional, quase sempre US$ 1. Funciona como um "dólar digital": circula em redes de blockchain, pode ser enviado a qualquer hora para qualquer país e é negociado em corretoras de criptoativos.

**Como mantém o valor:** a empresa que emite a stablecoin guarda reservas (dinheiro em banco e títulos do Tesouro americano) e promete trocar cada unidade por US$ 1. Se o preço cai abaixo de US$ 1, compensa comprar e resgatar; se sobe acima, compensa emitir e vender. Essa arbitragem segura o preço perto de US$ 1.

**USDT:** a stablecoin usada neste programa é o USDT, emitido pela empresa Tether. É a maior do mundo (cerca de US$ 180 bilhões em circulação em outubro de 2026, segundo a DefiLlama) e responde por quase 90% das operações com stablecoins declaradas à Receita Federal no Brasil.

| | Dólar no câmbio oficial | USDT (dólar digital) |
| --- | --- | --- |
| Onde se compra | Bancos e corretoras de câmbio | Corretoras de criptoativos (Binance, Mercado Bitcoin) |
| Horário | Dias úteis, horário comercial | 24 horas, todos os dias |
| Pagamento | Contrato de câmbio, IOF | Pix em reais |
| Preço de referência | PTAX, calculada pelo Banco Central | Definido pela oferta e procura em cada corretora |
| Quem garante | Sistema bancário regulado | A empresa emissora e as suas reservas |

**Por que os brasileiros usam:** proteger a poupança da desvalorização do real, fazer pagamentos e transferências internacionais e operar outros criptoativos.

**Riscos:** depende da confiança nas reservas do emissor; pode perder a paridade em crises; e a regulação ainda está em construção. No Brasil, o Banco Central passou a regular as prestadoras de serviços de ativos virtuais com as Resoluções 519, 520 e 521 (novembro de 2025) e a tratar parte das operações com stablecoins como operações de câmbio.

**Por que importa para o programa:** como o USDT é negociado em reais nas corretoras brasileiras, o seu preço revela quanto as pessoas estão dispostas a pagar pelo dólar fora do câmbio oficial. A diferença entre esse preço e o dólar oficial é o ágio, explicado a seguir.

## O que é ágio

**Ágio** é quanto um ativo está sendo negociado **acima** do seu preço de referência, em porcentagem. Quando o preço fica **abaixo** da referência, o nome é **deságio** (ágio negativo). Em inglês, o termo usual é *premium* (e *discount* para o deságio).

Neste programa, o ativo é o USDT (um dólar digital que promete valer sempre US$ 1) e a referência é o dólar oficial do Banco Central (PTAX). Em teoria, os dois deveriam custar o mesmo em reais; a diferença é o ágio.

```math
\text{ágio} = \frac{\text{preço do USDT em reais}}{\text{PTAX}} - 1
```

| Situação | PTAX | USDT nas corretoras | Ágio | Leitura |
| --- | --- | --- | --- | --- |
| Ágio positivo | R$ 5,00 | R$ 5,05 | +1,0% | Quem compra dólar digital paga 1% a mais que o oficial |
| Sem ágio | R$ 5,00 | R$ 5,00 | 0% | Os dois mercados estão alinhados |
| Deságio | R$ 5,00 | R$ 4,98 | −0,4% | O dólar digital está mais barato que o oficial |

**Uma analogia:** o mesmo ingresso de show vendido na bilheteria oficial e por revendedores. Se muita gente quer o ingresso e a bilheteria não atende a todos, o revendedor cobra mais caro; essa diferença é o ágio. Se sobram ingressos, o revendedor precisa vender abaixo do preço oficial: deságio.

**Por que o ágio existe, se é "o mesmo dólar":** levar dinheiro de um mercado para o outro tem custo, demora e regras (câmbio, impostos, limites). Enquanto esse atrito existe, os dois preços podem ficar diferentes. Quando muita gente procura dólar digital ao mesmo tempo, o ágio tende a subir; quando muitos vendem, tende a cair.

**Por que isso interessa:** o ágio funciona como um termômetro da procura por dólar fora do sistema oficial de câmbio. O programa mede esse termômetro todos os dias e testa a que tipo de notícia ele reage.

**Ágio anormal:** o ágio "normal" muda com o tempo (era cerca de 1% em 2020 e 0,2% em 2026). Por isso as análises usam o ágio do dia menos o ágio típico das 12 semanas anteriores: o quanto aquele dia fugiu do comum.

## Como funciona

O programa trabalha em quatro etapas, sempre na mesma ordem. Cada etapa lê o que a anterior gravou em disco, o que permite refazer qualquer uma sem repetir as outras.

1. **Coleta (camada bruta):** baixa os dados das APIs e grava as respostas exatamente como vieram, em `dados/bruto/`, com o horário da coleta. Nada nessa pasta é editado.
2. **Tratamento (camada tratada):** converte cada fonte numa tabela padronizada em CSV (`dados/tratado/`). Se o mesmo dia é coletado de novo, vale a coleta mais recente.
3. **Cálculo:** monta o ágio por corretora e consolidado, os sinais de comportamento e o painel diário.
4. **Análise e relatório:** roda os testes estatísticos, grava os resultados em `dados/resultados/` e gera gráficos e tabelas em `docs/`.

### Módulos

| Módulo | Função |
| --- | --- |
| `cli.py` | Linha de comando: recebe os comandos e os parâmetros e chama os demais módulos |
| `fontes/` | Um módulo por fonte (`bcb`, `binance`, `mercadobitcoin`, `tesouro`, `fred`, `google_trends`, `defillama`), cada um com `baixar()` e `tratar()` |
| `http.py` | Acesso às APIs com novas tentativas e pausas automáticas |
| `armazenamento.py` | Grava e lê as camadas bruta e tratada |
| `janela.py` | Preço do USDT na janela da PTAX (10h–13h de Brasília) |
| `indicador.py` | Cálculo do ágio e consolidação ponderada por volume |
| `comportamento.py` | Sinais de comportamento coletivo e painel diário |
| `analise.py` | Regressões, estudo de evento, permutação, robustez e quadro de hipóteses |
| `relatorio.py` | Gráficos e tabelas do trabalho |
| `episodio.py` | Diagnóstico de períodos de ágio fora do normal |
| `scripts/montar_eventos.py` | Gera a lista de 158 eventos a partir de uma regra fixa |
| `scripts/coleta_semanal.sh` | Coleta semanal automática (agendada no macOS) |

## Tecnologias

Linguagem **Python 3.10 ou mais recente** (testado em 3.13 e 3.14), sem servidor nem banco de dados: tudo roda no computador do pesquisador e grava arquivos CSV e JSON.

| Biblioteca | Versão mínima | Uso no programa |
| --- | --- | --- |
| pandas | 2.1 | Tabelas, datas, fusão das fontes, medianas móveis |
| statsmodels | 0.14 | Regressões por MQO com erros de Newey-West e regressão robusta de Huber |
| SciPy | 1.11 | Teste t e funções estatísticas |
| NumPy | (vem com o pandas) | Sorteios do teste de permutação e cálculos vetoriais |
| Matplotlib | 3.8 | Gráficos |
| Requests | 2.31 | Acesso às APIs públicas |
| pytest | 8 (só para desenvolvimento) | Testes automatizados |

**Outras ferramentas:** Git e GitHub (versionamento e publicação), setuptools (instalação como pacote, com o comando `agio`), launchd do macOS (agendamento da coleta semanal).

**Custo:** zero. Nenhuma fonte exige chave de acesso ou assinatura.

## Fontes de dados

| Fonte | Dado | Acesso | Cobertura |
| --- | --- | --- | --- |
| Banco Central (Olinda e SGS) | PTAX de venda (fechamento) e Selic diária | API pública | Todo o período |
| Binance | Candles diários e horários do USDT/BRL, número de negócios e volume comprado pelo agressor | `data-api.binance.vision` | Desde 13/10/2020 |
| Mercado Bitcoin | Candles diários e horários do USDT/BRL | API pública v4 | Desde 11/03/2023 |
| Tesouro Transparente | Taxas de compra dos títulos Tesouro IPCA+ (juro real de 10 anos) | CSV público, cerca de 14 MB | Todo o período |
| Cboe (FRED como alternativa) | VIX, fechamento diário | CSV público | Todo o período |
| Google Trends | Interesse de busca por "dólar" e "USDT" no Brasil | CSV exportado à mão | Diário, 11 janelas encadeadas |
| DefiLlama | Oferta global de USDT em circulação | API pública | Desde 2017 (uso exploratório) |

O programa trata as diferenças de formato de cada fonte (por exemplo, "<1" no Google Trends, "." como valor ausente no FRED, datas em formatos diferentes) dentro do `tratar()` de cada módulo. Se uma fonte mudar o formato, só esse trecho precisa de ajuste.

**Google Trends, passo a passo.** Não há API oficial estável, então a importação é por CSV: em trends.google.com, escolha Brasil, os termos e janelas de até 8 meses (janelas maiores viram dados semanais), sobrepostas em pelo menos 30 dias; exporte "Interesse ao longo do tempo" para `dados/manual/google_trends/`, um arquivo por janela; rode `agio importar-trends` e `agio calcular`.

## Instalação

Requisitos: Python 3.10 ou mais recente e Git. Funciona em macOS, Linux e Windows.

```bash
git clone https://github.com/augustojrezende/agio-stablecoin.git
cd agio-stablecoin
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest                             # 41 testes, sem acesso à rede
```

Depois disso, o comando `agio` fica disponível no terminal enquanto o ambiente virtual (`.venv`) estiver ativo. Todas as datas usam o formato `AAAA-MM-DD`.

## Comandos e parâmetros

Forma geral: `agio <comando> [parâmetros]`. `agio <comando> --help` mostra os parâmetros de cada um.

### Coleta

| Comando | O que faz | Parâmetros |
| --- | --- | --- |
| `coletar` | Baixa a PTAX, a Selic e os candles diários do USDT/BRL das corretoras | `--inicio` (obrigatório): primeiro dia; `--fim` (opcional): último dia, padrão = hoje |
| `coletar-horario` | Baixa os candles horários e calcula o preço na janela da PTAX | `--inicio` (obrigatório); `--fim` (opcional, padrão = hoje) |
| `coletar-controles` | Baixa o histórico do juro real de 10 anos (Tesouro) e do VIX (FRED ou, se falhar, Cboe) | `--so-vix`: só o VIX; `--so-juro`: só o juro real (não podem ser usados juntos; sem nenhum, baixa os dois) |
| `importar-trends` | Lê os CSVs do Google Trends em `dados/manual/google_trends/` e encadeia as janelas numa série única | Nenhum |

### Cálculo

| Comando | O que faz | Parâmetros |
| --- | --- | --- |
| `calcular` | Calcula o ágio (janela da PTAX e fechamento), os sinais de comportamento e o painel diário | Nenhum |
| `grafico` | Gráfico rápido do ágio por corretora (`dados/grafico_agio.png`) | Nenhum |

### Análise

| Comando | O que faz | Parâmetros |
| --- | --- | --- |
| `testar` | Teste formal: regressões (ágio, negócios, ticket e repasse), estudo de evento (lista completa e sem sobrepostos) e quadro de hipóteses V1 a V6 com correção de Holm | `--inicio` (opcional): só dias a partir desta data; `--fim` (opcional): só dias antes desta data. Sem os dois, usa todo o período. Com eles, é a validação fora da amostra (resultados numa pasta própria) |
| `robustez` | Repete a regressão do ágio em 9 especificações alternativas | Nenhum |
| `buscas` | Exploratório: buscas no Google em torno dos eventos e como antecipação do ágio | Nenhum (exige `importar-trends` e `calcular` antes) |
| `oferta-usdt` | Exploratório: oferta global de USDT como variável na regressão do ágio | `--sem-coleta`: usa a oferta já baixada, sem acessar a DefiLlama |
| `episodio` | Diagnóstico de um período de ágio fora do normal, contra os 90 dias anteriores | `--inicio` e `--fim` (ambos obrigatórios): início e fim do período |

### Relatório

| Comando | O que faz | Parâmetros |
| --- | --- | --- |
| `relatorio` | Gera os gráficos (`docs/figuras/`) e as tabelas (`docs/resultados_tabelas.md`) a partir dos resultados | Nenhum (exige `testar` e `robustez` antes) |

### Scripts auxiliares

| Script | O que faz |
| --- | --- |
| `python scripts/montar_eventos.py` | Gera `dados/manual/eventos.csv` (158 eventos) a partir da regra registrada no diário |
| `./scripts/coleta_semanal.sh` | Coleta os últimos 10 dias, recalcula o ágio e grava um log em `dados/logs/` |
| `./scripts/agendar_coleta_mac.sh` | Agenda a coleta semanal no macOS (segunda-feira, 20h) |

### Constantes ajustáveis no código

Não são parâmetros de linha de comando; foram fixadas antes dos testes e estão registradas no diário de decisões.

| Constante | Valor | Onde |
| --- | --- | --- |
| Janela da PTAX | 10h a 13h de Brasília | `janela.py` |
| Janela do "normal" do ágio anormal | 60 dias úteis (mínimo de 30) | `analise.py` |
| Janela do estudo de evento | −1 a +3 dias úteis | `analise.py` |
| Exclusão do placebo | 4 dias úteis em torno de cada evento | `analise.py` |
| Defasagens de Newey-West | 5 | `analise.py` |
| Sorteios da permutação | 5.000, semente 42 | `analise.py` |

## Uso típico

### Reproduzir os resultados do TCC do zero

```bash
agio coletar --inicio 2020-10-01            # preços diários, PTAX e Selic (alguns minutos)
agio coletar-horario --inicio 2020-10-01    # preços horários para a janela da PTAX
agio coletar-controles                      # juro real e VIX
agio importar-trends                        # opcional: buscas do Google (CSVs em dados/manual/google_trends)
agio calcular                               # ágio, sinais e painel diário
agio testar                                 # teste formal
agio robustez                               # 9 especificações
agio relatorio                              # gráficos e tabelas
```

Para reproduzir só a amostra do TCC (até 30/10/2026), use `--fim 2026-10-31` nos comandos de coleta.

### Manter a série atualizada

```bash
./scripts/coleta_semanal.sh       # teste manual
./scripts/agendar_coleta_mac.sh   # agenda toda segunda às 20h (macOS)
```

A coleta é idempotente: rodar de novo o mesmo período só substitui pelos dados mais recentes. As APIs das corretoras nem sempre guardam histórico longo, então a coleta precisa continuar regularmente.

### Validação fora da amostra (pré-registro)

```bash
agio testar --inicio 2026-11-02 --fim 2027-10-30   # intermediária (α = 1%)
agio testar --inicio 2026-11-02 --fim 2028-11-01   # final (α = 5%)
```

### Investigar um período específico

```bash
agio episodio --inicio 2026-06-01 --fim 2026-08-15
```

## Arquivos gerados

| Pasta | Arquivos principais | Conteúdo |
| --- | --- | --- |
| `dados/bruto/` | Um JSON ou CSV por coleta, com data e hora no nome | Respostas das APIs como vieram (não editar) |
| `dados/tratado/` | `ptax.csv`, `precos_usdt_brl.csv`, `precos_janela_ptax.csv`, `juro_real_10a.csv`, `vix.csv`, `google_trends.csv`, `usdt_oferta.csv` | Fontes padronizadas, uma linha por dia (e por corretora) |
| `dados/tratado/` | `agio_diario.csv`, `agio_por_fonte.csv`, `agio_fechamento_diario.csv` | O indicador: medida principal (janela da PTAX) e comparação (fechamento) |
| `dados/tratado/` | `sinais_comportamento.csv`, `painel_diario.csv` | Negócios, pressão compradora, ticket médio, buscas e ágio num só painel |
| `dados/manual/` | `eventos.csv`, `google_trends/*.csv` | Lista de eventos (gerada por script) e exportações do Google Trends |
| `dados/resultados/` | `relatorio.txt`, `regressao_*.csv`, `eventos_*.csv`, `hipoteses.csv`, `robustez.csv`, `base_teste.csv` | Resultados de cada teste |
| `dados/resultados/` | `exploratorio_*.csv` e `.txt`, `episodio_*.csv` | Análises exploratórias e diagnósticos |
| `docs/figuras/` | `01_serie_agio.png` a `09_buscas_*.png` | Gráficos do trabalho |
| `docs/` | `resultados.md`, `resultados_tabelas.md`, `decisoes.md`, `pre-registro.md` | Relatório narrativo, tabelas automáticas, diário de decisões e pré-registro |
| `dados/logs/` | `coleta_*.log` | Registro de cada coleta semanal |

## Métodos implementados

### Ágio na janela da PTAX

Para cada dia e corretora, o preço é a média dos preços típicos dos candles horários entre 10h e 13h de Brasília, ponderada pelo volume; o preço típico de cada hora é (máxima + mínima + fechamento) / 3.

```math
A_{i,t} = \frac{P^{USDT}_{i,t}}{PTAX_t} - 1, \qquad A_t = \frac{\sum_i V_{i,t} A_{i,t}}{\sum_i V_{i,t}}
```

Em que *i* é a corretora, *t* o dia útil e *V* o volume negociado na janela.

### Ágio anormal

```math
AA_t = A_t - \operatorname{mediana}(A_{t-60}, \dots, A_{t-1})
```

A mediana usa só dias anteriores (mínimo de 30). A mesma transformação é aplicada ao log do número de negócios, do ticket médio e das buscas.

### Regressão principal

```math
AA_t = \alpha + \beta_1 \Delta d_t + \beta_2 \Delta j_t + \beta_3 \Delta VIX_t + \beta_4 \Delta VIX_{t-1} + \beta_5 \ln M_t + \varepsilon_t
```

Em que Δd é a variação diária da PTAX (100 × diferença de logs), Δj a variação do juro real de 10 anos em pontos-base, e M o volume mediano dos 60 dias anteriores. Estimação por MQO com erros de Newey-West (5 defasagens).

### Juro real de 10 anos

Para cada dia, as taxas de compra da manhã dos títulos Tesouro IPCA+ (sem cupom) são interpoladas linearmente no prazo de 10 anos.

### Estudo de evento

- **Efeito acumulado (CAR):** soma do ágio anormal de −1 a +3 dias úteis em torno de cada evento.
- **Teste de permutação:** 5.000 sorteios de datas sem eventos (fora de 4 dias úteis de qualquer evento), do mesmo tamanho do grupo; o p-valor é a fração de sorteios com média tão distante da média placebo quanto a dos eventos.
- **Domésticos × externos:** permutação dos rótulos entre os dois grupos.

### Robustez e testes múltiplos

- Winsorização nos percentis 1 e 99; regressão robusta de Huber (norma HuberT do statsmodels).
- Correção de Holm sobre as 7 hipóteses do pré-registro.

### Google Trends

Cada janela exportada vem normalizada de 0 a 100. As janelas sobrepostas são reescaladas pela razão entre as médias nos dias em comum com busca nos dois lados, formando uma série diária única por termo.

## Qualidade, reprodutibilidade e licenças

- **Testes automatizados:** 41 testes (pytest), que rodam sem rede, com dados sintéticos de efeito conhecido. Cobrem a leitura de cada fonte, o cálculo do ágio e da janela, a recuperação de efeitos conhecidos pela regressão e pelo estudo de evento, e os comandos de ponta a ponta.
- **Dados brutos imutáveis:** toda transformação sai do código; nada é editado à mão.
- **Lista de eventos por regra:** gerada por script, com a fonte de cada evento; 17 datas conferidas pelo pesquisador.
- **Diário de decisões** (`docs/decisoes.md`): cada escolha metodológica com data, motivo e erros encontrados e corrigidos.
- **Pré-registro** (`docs/pre-registro.md`): hipóteses e regras fixadas antes dos dados de validação, com adendo datado.
- **Separação explícita** entre análises confirmatórias e exploratórias nas saídas do programa.
- **Histórico completo no Git:** cada mudança entrou por pull request, com descrição.
- **Licenças:** código sob MIT; dados derivados (séries do ágio) sob Creative Commons Atribuição 4.0 (CC BY 4.0). Os dados de origem seguem os termos de cada fonte.

## Limitações e próximos passos

**Limitações:**

- Duas corretoras, com a Binance concentrando o volume; o indicador é, na prática, o da Binance.
- Dados agregados: medem comportamento coletivo, não motivações individuais.
- O juro real é uma medida indireta do estresse fiscal (o CDS ficou de fora por custo).
- O Google Trends exige exportação manual, e o Google reamostra os dados a cada consulta.
- A coleta depende de APIs públicas que podem mudar de formato ou limitar o histórico.

**Próximos passos:**

- Validação fora da amostra em out/2027 e out/2028.
- Novas corretoras e outras stablecoins (por exemplo, USDC).
- Migração do armazenamento para Parquet ou DuckDB quando a base crescer.
- Dados on-chain (fluxos na blockchain), na pesquisa de mestrado.

## Como citar

REZENDE, Augusto. *agio-stablecoin*: código e dados do ágio da stablecoin em reais. GitHub, 2026. Disponível em: https://github.com/augustojrezende/agio-stablecoin.

Trabalho associado: REZENDE, Augusto. *O ágio da stablecoin em reais*: reação a choques domésticos e externos no Brasil (2020–2026). Trabalho de Conclusão de Curso (Graduação em Ciências Econômicas). Em elaboração.
