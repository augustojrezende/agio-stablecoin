# Diário de decisões metodológicas

Cada entrada: data, decisão, motivo, alternativa descartada. Vira a seção de método do TCC.

## 2026-10-30 — Definição do indicador

- **Decisão:** ágio = fechamento diário do USDT/BRL ÷ PTAX de venda − 1.
- **Motivo:** a PTAX é a referência oficial e pública; o USDT concentra a maior parte do volume de stablecoins negociado em reais.
- **Descartado:** dólar comercial de mercado (fonte paga) e USDC como série principal (volume menor; pode entrar como robustez).

## 2026-10-30 — Dias considerados

- **Decisão:** ágio só em dias úteis com PTAX; preços de fim de semana ficam guardados.
- **Motivo:** não existe referência oficial no fim de semana.
- **A testar:** usar a PTAX do último dia útil para cobrir fins de semana em choques que começam no domingo (como o segundo turno de 2026).

## 2026-10-30 — Descasamento de horário

- **Decisão:** aceitar, por ora, o descasamento entre a PTAX (por volta das 13h de Brasília) e o fechamento do candle (21h de Brasília).
- **Motivo:** simplicidade na primeira versão; o efeito é ruído.
- **Próximo passo:** candles horários, pegando o preço por volta das 13h, para alinhar com a PTAX.

## 2026-10-30 — Consolidação entre corretoras

- **Decisão:** ágio diário consolidado ponderado pelo volume de cada corretora.
- **Motivo:** evita que uma corretora pequena e ilíquida domine o indicador.
- **Robustez:** manter o ágio por corretora em `agio_por_fonte.csv` para comparar.

## 2026-10-30 — Armazenamento

- **Decisão:** respostas brutas em JSON com horário da coleta; tabelas tratadas em CSV versionado no Git.
- **Motivo:** reprodutibilidade e diferenças legíveis no Git. Migrar para Parquet ou DuckDB quando a base crescer (mestrado).

## 2026-10-31 — Sinais de comportamento coletivo

- **Decisão:** incluir três sinais de mercado (pressão compradora, número de negócios, ticket médio em reais) e o interesse de busca do Google Trends.
- **Motivo:** completar a tríade economia, comportamento e TI, explicando por que o ágio sobe (medo, efeito manada, atenção), não só se sobe.
- **Limite:** dados agregados; o texto fala em comportamento coletivo, sem atribuir motivações individuais (falácia ecológica).
- **Descartado no TCC:** questionário com investidores (exige comitê de ética e alonga o prazo); fica para o mestrado.

## 2026-10-31 — Google Trends por CSV

- **Decisão:** importar CSVs exportados manualmente, em janelas de até 8 meses sobrepostas em 30 dias ou mais, encadeadas pela razão média na sobreposição.
- **Motivo:** bibliotecas não oficiais costumam ser bloqueadas e mudam sem aviso; o CSV é reproduzível e citável.
- **Cuidado:** guardar os CSVs originais no repositório e registrar a data de exportação, porque o Google reamostra os dados a cada consulta.

## 2026-10-31 — Ágio alinhado à janela da PTAX

- **Decisão:** a medida principal passa a usar o preço médio do USDT, ponderado pelo volume, entre 10h e 13h de Brasília (13h a 16h UTC), a mesma janela em que o Banco Central forma a PTAX. O ágio de fechamento (candle diário, 21h) fica como comparação.
- **Motivo:** na primeira coleta (out/2020 a out/2026), os menores ágios da série caíram justamente em dias de choque: 09/04/2025 (−3,5%), 26/10/2026 (−2,1%, dia seguinte ao segundo turno) e 06/11/2024 (−1,8%). A explicação provável é o horário: a PTAX registra o câmbio da manhã, e o fechamento das 21h registra o mercado já acalmado. O descasamento é maior exatamente nos dias que mais importam para o estudo.
- **Detalhes:** preço típico de cada hora, (máxima + mínima + fechamento) / 3, ponderado pelo volume; sem volume na janela, média simples dos fechamentos. O Brasil não tem horário de verão desde 2019, então a janela é fixa em UTC.
- **A verificar:** quantos dias ficam sem negociação na janela no início da série (2020–2021), quando o volume era baixo.

## 2026-10-31 — Resultados preliminares da série alinhada (out/2020 a out/2026)

*Análise descritiva, sem teste formal. Ágio anormal = ágio do dia menos a mediana dos 60 dias úteis anteriores.*

- **A correção de horário funcionou:** 09/04/2025 passou de −3,5% (fechamento) para cerca de 0% (janela da PTAX). A correlação entre as duas medidas é 0,54, e o desvio padrão de 2025 caiu de 0,53 para 0,19 p.p.
- **Custo:** a correlação entre corretoras caiu de 0,91 para 0,68, porque a janela de 3 horas tem menos negócios, sobretudo no Mercado Bitcoin. A consolidação por volume reduz o efeito.
- **Choques domésticos não elevaram o ágio:** pacote fiscal (29/11/2024, −1,5 p.p. anormal), segundo turno (26/10/2026, −0,8 p.p.). Primeiro turno (05/10/2026): +0,24 p.p.
- **O maior ágio anormal foi externo:** 05/08/2024, +3,0 p.p. (turbulência global).
- **A participação reage com força:** o número de negócios dobra ou triplica nas crises (dez/2024: 140 a 170 mil por dia contra cerca de 60 mil; 05/08/2024: 179 mil; 26/10/2026: 105 mil contra cerca de 46 mil), e o ticket médio cai (entrada do varejo).
- **Interpretação a testar:** quando o dólar oficial dispara, detentores de USDT vendem para realizar ganho e seguram o preço; a pressão compradora abaixo de 0,5 nesses dias é compatível.
- **Episódio a investigar:** de 24/06 a meados de julho de 2026, ágio entre 1% e 1,7% por semanas seguidas, sem paralelo na série. Verificar mudança tributária ou regulatória sobre stablecoins no período.
- **Possível reformulação da hipótese (só depois do teste formal):** o medo fiscal se manifestaria na participação no mercado de dólar digital, e não no prêmio de preço.

### Próximos testes

1. Regressão do ágio anormal controlando pela variação do dólar oficial no dia.
2. Janela da PTAX incluindo a hora das 13h: o Banco Central consulta às 10h, 11h, 12h e 13h, e a janela atual vai até 12h59.
3. Mesma análise de evento para o número de negócios e o ticket médio.

## 2026-10-31 — Teste formal: desenho e regra de decisão

- **Regressão (todos os dias, Newey-West com 5 defasagens):** ágio anormal ~ variação do dólar oficial + variação do juro real de 10 anos (bp) + variação do VIX (no dia e no anterior) + tamanho do mercado. O mesmo para número de negócios e ticket médio.
- **Juro real de 10 anos:** taxas de compra da manhã dos títulos Tesouro IPCA+ (sem cupom), interpoladas no prazo de 10 anos. Taxa da manhã para coincidir com a janela da PTAX.
- **VIX:** o fechamento em Nova York sai depois da janela da PTAX; por isso entram a variação do dia e a do dia anterior.
- **Estudo de evento:** janela de −1 a +3 dias úteis; ágio anormal acumulado; teste t e teste de permutação contra datas sorteadas fora de ±10 dias úteis dos eventos; comparação domésticos (fiscal, político) x externos por permutação de rótulos.
- **Ágio ajustado pelo dólar:** resíduo da regressão do ágio anormal sobre a variação do dólar, para o estudo de evento não confundir o efeito mecânico do câmbio com reação ao medo.
- **Regra de decisão:** hipótese original confirmada se o coeficiente do juro real for positivo e significativo a 5% e os domésticos tiverem ágio anormal maior que os externos; versão comportamental confirmada se a participação for significativamente maior nas crises.
- **Lista de eventos:** rascunho com 15 eventos marcados como A CONFIRMAR; a versão final deve ser fixada, com fontes, antes de interpretar os resultados.

## 2026-10-31 — Primeira rodada do teste (sem juro real e VIX)

- **Efeito mecânico do dólar confirmado:** coeficiente de −0,11 (t = −9,6): cada 1% de alta do dólar oficial no dia reduz o ágio em 0,11 p.p. O controle é indispensável.
- **Estudo de evento com 15 eventos:** nenhum grupo significativo, nem no ágio nem no número de negócios. Nos negócios, o teste t contra zero dá p = 0,013 para todos os eventos, mas a permutação dá p = 0,25: o número de negócios anormal é positivo em média (mercado em crescimento), e a comparação certa é com datas sorteadas.
- **Leitura:** com 2 a 6 eventos por grupo, o teste tem pouco poder. Prioridade: ampliar a lista (todas as reuniões do Copom, anúncios fiscais) e incluir juro real e VIX.

## 2026-11-01 — Rodada completa (com juro real e VIX)

*1.490 dias úteis; MQO com Newey-West (5 defasagens); variável dependente: ágio anormal (p.p.). VIX pela Cboe (FRED fora do ar).*

| Variável | Coeficiente | p-valor |
| --- | --- | --- |
| Variação do dólar oficial (%) | −0,129 | < 0,001 |
| Variação do juro real 10 anos (bp) | +0,0019 | 0,088 |
| Variação do VIX no dia | +0,021 | 0,047 |
| Variação do VIX no dia anterior | +0,016 | 0,008 |
| Tamanho do mercado (log) | +0,029 | 0,087 |

R² = 0,095; curtose dos resíduos = 15,3 (poucos dias extremos pesam muito).

- **Regra de decisão aplicada:** a hipótese original **não se confirma**. O coeficiente do juro real é positivo, mas só significativo a 10%, e pequeno: um choque fiscal de +20 bp move o ágio em cerca de 0,04 p.p. No estudo de evento, os domésticos não têm ágio maior que os externos (diferença −0,58 p.p., p = 0,60).
- **Medo global:** as duas variações do VIX são significativas. Um salto de 10 pontos eleva o ágio em cerca de 0,2 p.p. no dia e 0,15 p.p. no seguinte. O VIX do dia anterior é o resultado mais limpo, porque é conhecido antes da janela da PTAX.
- **Participação:** número de negócios anormal sem relação com juro real nem VIX no dia a dia (só o tamanho do mercado é significativo). Ticket médio cai quando o dólar sobe (−0,012, p = 0,044), compatível com entrada do varejo.
- **Estudo de evento:** inalterado (15 eventos provisórios, nenhum grupo significativo pela permutação).
- **Interpretação provisória (a testar):** em pânicos globais, investidores de criptoativos migram das moedas voláteis para stablecoins, e a demanda por USDT eleva o ágio. O dólar digital funcionaria mais como proteção contra o medo global do que contra o medo fiscal doméstico.
- **Conclusão provisória:** o ágio do dólar digital em reais reage mais ao medo global do que ao medo fiscal doméstico; o estresse fiscal mexe pouco no preço e aparece sobretudo no aumento da participação em grandes choques.
- **Antes de tratar como resultado final:** (1) fechar a lista de eventos com fontes; (2) robustez (`agio robustez`): winsorização, regressão de Huber, ágio de fechamento, cada corretora, antes e depois de 04/05/2026, janela incluindo a consulta das 13h.

## 2026-11-01 — Testes de robustez

*`agio robustez`; variável dependente: ágio anormal (p.p.). Coeficiente (p-valor).*

| Especificação | n | Juro real (bp) | VIX no dia | VIX dia anterior | Dólar oficial |
| --- | --- | --- | --- | --- | --- |
| 1. Principal (janela 10h-13h, Newey-West) | 1.490 | 0,0019 (0,088) | 0,021 (0,047) | 0,016 (0,008) | −0,129 (< 0,001) |
| 2. Winsorizada 1%/99% | 1.490 | 0,0015 (0,171) | 0,011 (0,062) | 0,011 (0,028) | −0,121 (< 0,001) |
| 3. Regressão robusta (Huber) | 1.490 | 0,0014 (0,055) | 0,007 (0,017) | 0,009 (0,004) | −0,098 (< 0,001) |
| 4. Ágio de fechamento (21h) | 1.490 | −0,0071 (0,001) | 0,101 (< 0,001) | 0,021 (0,016) | −0,040 (0,082) |
| 5a. Só Binance | 1.490 | 0,0019 (0,089) | 0,021 (0,046) | 0,016 (0,007) | −0,130 (< 0,001) |
| 5b. Só Mercado Bitcoin | 884 | −0,0005 (0,753) | 0,014 (0,378) | 0,007 (0,367) | −0,091 (< 0,001) |
| 6a. Antes de 04/05/2026 | 1.363 | 0,0019 (0,141) | 0,023 (0,040) | 0,017 (0,005) | −0,136 (< 0,001) |
| 6b. A partir de 04/05/2026 | 127 | −0,0013 (0,671) | −0,012 (0,597) | −0,005 (0,845) | −0,061 (0,111) |
| 7. Janela 10h-14h (inclui a consulta das 13h) | 1.490 | 0,0006 (0,590) | 0,025 (0,007) | 0,012 (0,027) | −0,105 (< 0,001) |

- **Medo global robusto:** o VIX do dia anterior é significativo a 5% em 7 das 9 especificações, inclusive com os extremos atenuados (winsorização e Huber); o resultado não depende de poucos dias. Ausências explicáveis: Mercado Bitcoin (série desde 2023 e pouca negociação na janela) e o período pós-04/05/2026 (127 dias, sem poder estatístico; não é possível afirmar mudança com a regulação).
- **Medo fiscal frágil:** o juro real nunca é positivo e significativo a 5%. Com a janela até 14h, cai para 0,0006 (p = 0,59). No ágio de fechamento é significativo, mas negativo; essa medida tem o descasamento de horário que motivou a janela da PTAX (o efeito do dólar cai de −0,13 para −0,04), então não é evidência a favor da hipótese.
- **Efeito mecânico do dólar:** negativo e forte em todas as especificações alinhadas à PTAX.
- **Peso da Binance:** a especificação só Binance é praticamente idêntica à principal; o indicador consolidado é, na prática, a Binance, que concentra o volume. Registrar na metodologia.
- **Decisão:** pela regra fixada antes do teste, a hipótese original (o ágio como termômetro do estresse fiscal) é rejeitada; o resultado principal passa a ser a sensibilidade do ágio ao medo global. Falta fechar a lista de eventos para concluir o estudo de evento e a parte comportamental.

## 2026-11-01 — Lista de eventos fechada por regra

- **Motivo:** a lista provisória tinha 15 eventos escolhidos um a um, e os resultados já tinham sido vistos. Para não escolher, mesmo sem querer, os dias que "funcionam", a lista passa a sair de uma regra fixa, aplicada a todo o período (out/2020 a out/2026), gerada por `scripts/montar_eventos.py`.
- **Regra:**
  - **Monetário (agendado):** toda decisão do Copom.
  - **Externo (agendado):** toda decisão do Fed (FOMC).
  - **Fiscal (agendado):** envio do PLDO (até 15/04) e do PLOA (até 31/08) e cada Relatório de Avaliação de Receitas e Despesas Primárias (22º dia após o bimestre). Relatórios extemporâneos ficam de fora.
  - **Fiscal (não agendado):** anúncios de mudança nas regras fiscais ou de medida extraordinária para cumprir a meta, com notícia que comprove a data: teto/Auxílio Brasil (21/10/2021), PEC da Transição (16/11/2022), arcabouço (30/03/2023), pacote fiscal (27/11/2024), IOF (22/05/2025). Nenhum anúncio desse tipo encontrado em 2026.
  - **Político (agendado):** os turnos das eleições presidenciais de 2022 e 2026.
  - **Externo (não agendado):** os choques da lista provisória, com fonte.
  - **Regulatório:** normas do Banco Central sobre criptoativos e stablecoins (publicação, vigência, início de obrigações e adiamentos).
- **Data do evento:** primeiro dia em que a janela da PTAX (10h-13h) pode reagir. Anúncio depois das 13h ou fora do pregão vai para o dia seguinte. Copom (18h30) e Fed (14h de Nova York) caem sempre no dia útil seguinte. `data_anuncio` guarda a data original.
- **Resultado:** 158 eventos (55 externos, 48 monetários, 47 fiscais, 4 políticos, 4 regulatórios); 145 agendados e 13 não agendados.
- **Sobreposição:** 93 eventos têm outro evento de tipo diferente a até 4 dias úteis (sobretudo Copom e Fed na mesma semana). O teste roda com a lista completa e sem os sobrepostos.
- **Placebo:** a exclusão em torno dos eventos passa de 10 para 4 dias úteis (o mínimo para a janela placebo não cruzar a de um evento); com 10, quase não sobrariam datas para sortear.
- **Correções da lista provisória:** a pausa nas tarifas dos EUA foi anunciada às 14h de 09/04/2025, depois da janela, e passa para 10/04. O evento de 04/05/2026 era o início previsto das obrigações de informação da Resolução 521; a Resolução 574 (18/06/2026) adiou o reporte de operações com ativos virtuais no câmbio para 03/11/2026. O corte de robustez em 04/05/2026 continua, mas deve ser lido como "início previsto", não como mudança efetiva.
- **Pendente de conferência:** as datas do PLDO, do PLOA e dos relatórios bimestrais seguem o prazo legal; a data efetiva de cada um ainda precisa ser conferida (a janela de −1 a +3 tolera pequenas diferenças).
- **Compromisso:** rodar `agio testar` uma vez com esta lista e aceitar o resultado. Mudanças posteriores na lista precisam de registro aqui, com o motivo.

## 2026-11-01 — Resultado da lista fechada e validação fora da amostra

- **Estudo de evento com a lista fechada (154 eventos usados):** nenhum grupo difere das datas sorteadas (ágio, todos: p = 0,36; domésticos − externos: p = 0,77; negócios, todos: p = 0,63). Sem sobrepostos (62), os choques externos isolados reduzem o ágio ajustado (−0,61 p.p., p = 0,035), resultado exploratório entre cerca de 40 testes.
- **Regra de decisão:** nem a hipótese original nem a comportamental se confirmam na amostra de descoberta. Detalhes em `resultados.md`.
- **Decisão do pesquisador:** o TCC mantém a hipótese fiscal como hipótese principal, testada e documentada até o fim. Os resultados que surgiram na análise (medo global e repasse incompleto do câmbio) ficam como ponto de partida para o mestrado.
- **Validação fora da amostra:** hipóteses V1 a V5 e regras registradas em `pre-registro.md` antes de qualquer dado posterior a 30/10/2026. Análise intermediária em 30/10/2027 (α = 1%) e final em 31/10/2028 (α = 5%), cada uma rodada uma vez.
- **Documentação:** `resultados.md` (narrativa), `agio relatorio` (8 figuras e tabelas), `agio testar` passa a gravar o quadro das hipóteses com p-valores de Holm.

## 2026-11-01 — Novo título

- **Antes:** "O ágio da stablecoin em reais: um termômetro do estresse fiscal no Brasil (2020–2026)".
- **Agora:** "Medo fiscal ou medo global? O ágio da stablecoin em reais diante de choques domésticos e externos (2020–2026)".
- **Motivo:** a pergunta passa de "é um termômetro fiscal?" para "qual medo move o ágio?". A comparação entre choques domésticos e externos já estava no desenho original, antes dos resultados.
- **O que não muda:** a hipótese fiscal continua sendo a principal e é testada por inteiro; dados, testes, regra de decisão e pré-registro ficam iguais. Mudam a pergunta, o objetivo geral e a forma de apresentar as hipóteses na introdução e na conclusão.

## 2026-11-01 — Episódio de ágio alto (24/06 a meados de julho de 2026): investigação

*Ágio de 1% a 1,7% por semanas, sem paralelo na série. Antes de buscar causa econômica, checar se é medição: `agio episodio --inicio 2026-06-01 --fim 2026-08-15`.*

**Pesquisa no noticiário (nenhuma causa única encontrada):**
- **Dólar subiu em junho** (+2,4% no mês; +1,9% em 18/06). Pelo efeito mecânico já medido, dólar em alta *reduz* o ágio; o episódio aconteceu apesar disso.
- **Resolução BCB 574 (18/06/2026):** adiou para 03/11/2026 o reporte de operações com ativos virtuais no câmbio. Uma semana antes do início; o sentido do efeito não é óbvio (adiamento reduz atrito).
- **IOF sobre stablecoins:** proposta de até 3,5% noticiada em mar/2026; a consulta pública foi adiada (Reuters, 23/03/2026). Nenhuma notícia de decreto em junho ou julho. Expectativa de imposto poderia antecipar compras, mas não há data que coincida.
- **Resolução BCB 561 (publicada por volta de 30/04/2026):** proíbe liquidar pagamentos internacionais eFX com stablecoins, a partir de 01/10/2026. Longe do episódio.
- **Saída de corretoras:** NovaDAX anunciou o encerramento no Brasil em 08/06/2026 (por decisão do grupo controlador); as demais saídas são de agosto a outubro, ligadas ao prazo de autorização de 30/10/2026. Não afeta Binance nem Mercado Bitcoin diretamente.

**Próximo passo:** rodar o diagnóstico e verificar (1) se o ágio alto aparece nas duas corretoras, (2) na janela e no fechamento, (3) se veio de alta do USDT ou de queda da PTAX, (4) liquidez na janela e (5) pressão compradora e número de negócios.

Fontes: [Resolução 574](https://www.letsmoney.com.br/noticias/bc-adia-novembro-reporte-cripto-cambio-resolucao-574/), [consulta do IOF adiada](https://investnews.com.br/investimentos/governo-deve-adiar-consulta-sobre-iof-em-criptomoedas-diz-reuters/), [Resolução 561](https://www.moneytimes.com.br/resolucao-do-banco-central-limita-uso-de-stablecoins-no-brasil-investidor-deve-se-preocupar-rens/), [vigência da 561](https://whale-alert.io/stories/8bae01a704e36c/Brazil-bans-crypto-in-regulated-crossborder-eFX-payments-measures-take-effect-Oct-1-2026), [corretoras que saíram](https://brasilbitcoin.com.br/blog/corretoras-criptomoedas-encerrando-operacoes-brasil/), [dólar em junho](https://www.dgabc.com.br/Noticia/4332380/dolar-tem-leve-queda-para-r-5-16-mas-fecha-junho-com-valorizacao-de-2-38).
