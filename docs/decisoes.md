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
- **Pendente de conferência:** as datas do PLDO, do PLOA e dos relatórios bimestrais seguem o prazo legal; a data efetiva de cada um ainda precisa ser conferida (a janela de −1 a +3 tolera pequenas diferenças). *Conferida por amostragem no mesmo dia; registro em 2026-11-07.*
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

## 2026-11-01 — Episódio de jun-jul/2026: diagnóstico e teste exploratório

- **Diagnóstico (`agio episodio`):** o ágio alto aparece nas duas corretoras (correlação 0,83), na janela e no fechamento, com liquidez normal na janela (volume 52% maior). Veio da alta do USDT com a PTAX parada; a convergência levou cerca de 4 semanas. Ticket médio 39% maior, número de negócios igual e pressão compradora menor. **Conclusão: fenômeno de mercado, não erro de medição.** Padrão compatível com escassez de vendedores e arbitragem lenta.
- **Hipótese exploratória:** contração da oferta global de USDT em junho de 2026 (≈ US$ 190 bi → 184 bi; [Cryptonomist](https://en.cryptonomist.ch/2026/07/28/stablecoin-market-dynamics-june-2026/)).
- **Decisão:** coletar a oferta diária de USDT (DefiLlama, gratuita) e testar, **fora do pré-registro e só na amostra de descoberta**, se a variação de 5 dias da oferta (com 1 dia de defasagem) explica o ágio anormal; sinal esperado negativo. Resultado será apresentado como exploratório no TCC e, se relevante, vira hipótese pré-registrada do mestrado. O teste principal e o pré-registro do TCC não mudam.

## 2026-11-01 — Oferta global de USDT: resultado do teste exploratório

- **Resultado (`agio oferta-usdt`, amostra de descoberta, 1.490 dias):** variação de 5 dias da oferta de USDT, +0,031 (p = 0,051). Sinal oposto ao previsto (negativo).
- **Oferta no fim do mês (US$ bi):** mai 188,4; jun 185,0; jul 183,5; out 180,1. A queda de outubro, maior que a de junho, não trouxe novo salto do ágio.
- **Decisão:** a hipótese da escassez global de USDT é descartada como explicação do episódio de jun-jul/2026. O sinal positivo sugere que a oferta acompanha a demanda (emissão quando a procura sobe). A causa do episódio fica em aberto (provável atrito local de arbitragem) e passa a ser uma pergunta do mestrado.
- **Robustez lateral:** com a oferta na regressão, VIX (p = 0,045 e 0,008) e dólar (−0,128) não mudam; juro real a p = 0,118.
- A variável não entra no teste principal nem no pré-registro.

## 2026-11-01 — Figuras publicadas, repasse defasado e adendo ao pré-registro

- **Figuras e tabelas da descoberta** publicadas em `docs/figuras/` e `docs/resultados_tabelas.md` (commit do pesquisador).
- **Repasse defasado:** soma das defasagens do dólar = −0,080 (p < 0,001), sinal oposto ao previsto na V4b. O ágio continua caindo por dois dias depois de uma alta do dólar, o que é compatível com realização de ganhos.
- **Decisão (aprovada pelo pesquisador):** adendo 1 ao pré-registro. A V4b é mantida como escrita, e entra a V6 (soma < 0), derivada da descoberta. A correção de Holm passa a cobrir 7 hipóteses, e o quadro mostra `confirma` e `confirma_holm`.
- **Dias extremos do dólar** conferidos: 26/10/2026 (+8,8%), 05/10/2026, 03/10/2022 e 09/11/2020 são reais, todos depois de fim de semana e ligados a eleições ou choques conhecidos. Nenhum dado corrigido.
- **Legenda da Figura 5:** a reta é simples, sem controles (−0,109), e difere do coeficiente da regressão (−0,129).

## 2026-11-01 — Google Trends importado

- **Exportação:** 22 CSVs em 01/11/2026 (Brasil, dados diários), 11 janelas de cerca de 8 meses de set/2020 a out/2026, sobrepostas em 30 a 31 dias. "dólar" e "comprar dólar" numa consulta; "USDT" em outra, para não perder resolução.
- **Correção no encadeamento:** termos exportados em arquivos separados passaram a ser encadeados só entre as janelas que os contêm. A razão de escala usa apenas os dias da sobreposição com busca nos dois lados.
- **"comprar dólar" fica de fora:** quase todos os dias aparecem como 0 ou "<1" ao lado de "dólar" (só 2 dias com busca na primeira sobreposição), então não é possível encadear com segurança. Se for necessário, exportar o termo sozinho.
- **Séries resultantes ("dólar" e "USDT", 2.252 dias):** os picos coincidem com choques conhecidos (06/11/2024, eleição nos EUA; dez/2024, dólar recorde; 26/10/2026, dia seguinte ao segundo turno), o que valida o encadeamento.

## 2026-11-01 — Atenção do público (Google Trends): análise exploratória

- **Decisão:** incluir no TCC uma análise curta (uma figura e uma tabela), fora do pré-registro e só na amostra de descoberta, com duas perguntas: (1) as buscas por "dólar" e "USDT" sobem nos eventos mais do que em datas sorteadas? (2) as buscas do dia anterior antecipam o ágio?
- **Medida:** buscas anormais = log(1 + interesse) menos a mediana dos 60 dias úteis anteriores, a mesma lógica do ágio anormal.
- **Motivo:** completar a parte comportamental sem alongar o trabalho; a atenção mede o "medo" do público diretamente, o que o número de negócios não faz.

## 2026-11-01 — Atenção do público: resultado

- **Buscas por "dólar":** sobem nos eventos externos (+0,38, p = 0,013), políticos (+3,01, p < 0,001, n = 4) e não agendados (+1,12, p < 0,001); não nos fiscais (+0,07, p = 0,92).
- **Buscas por "USDT":** não diferem das datas sorteadas (todos: p = 0,29).
- **Antecipação:** as buscas do dia anterior não explicam o ágio (USDT p = 0,13; dólar p = 0,21).
- **Leitura registrada em `resultados.md` (7.1):** a atenção do público responde a choques externos e políticos, não a anúncios fiscais, e não vira procura por dólar digital. Resultado exploratório.

## 2026-11-01 — Título final

- **Agora:** "O ágio da stablecoin em reais: reação a choques domésticos e externos no Brasil (2020–2026)".
- **Antes:** "Medo fiscal ou medo global? O ágio da stablecoin em reais diante de choques domésticos e externos (2020–2026)".
- **Motivo:** títulos acadêmicos evitam interrogação, e "medo fiscal" e "medo global" são a interpretação do resultado, não o objeto do estudo. O título passa a nomear o objeto (o ágio) e o que se compara (choques domésticos e externos). Hipóteses, testes e pré-registro não mudam.

## 2026-11-05 — Auditorias, versão corrigida e congelamento

- **Auditorias (02/11/2026):** AUD-001 (diagnóstico), AUD-002 (correção numa cópia separada) e AUD-003 (parecer final, aprovado com ressalvas). Relatórios em `auditorias/`. Parecer independente sobre as três em 05/11/2026, também aprovado com ressalvas.
- **Incorporação:** a versão corrigida (V2) entra no repositório com os caminhos de sempre (`dados/resultados`, `dados/manual/eventos.csv`, `docs/figuras`). A versão original fica na tag `descoberta-v1`.
- **Sete erros corrigidos:** robustez com índices duplicados, calendário das sobreposições, mínimo de eventos da V1, família de Holm, mediana da Figura 1, n das trajetórias e unidade do volume. Nenhum mudou a regressão principal, a robustez ou a decisão das hipóteses. A lista isolada passou de 62 para 60 eventos.
- **Calendário das sobreposições pela PTAX:** `scripts/montar_eventos.py` passou a usar os dias com PTAX publicada (`calendario_ptax`), e não `base_teste.csv`, que só existe depois de rodar o teste. Gera a mesma lista da V2 (conferido: 158 eventos idênticos).
- **Rótulo da V6:** "Ágio segue caindo após alta do dólar". O teste não muda.
- **Placebos temporais na lista corrigida:** com rótulos embaralhados dentro de cada ano, p = 0,091 (ajustado) e 0,135 (anormal); com deslocamento das séries dentro do ano, p = 0,086 e 0,107. O contraste dos isolados (p = 0,031 e 0,043) não resiste. Diagnóstico, não nova especificação.
- **Reprodução:** com os caminhos de sempre, `agio testar` e `agio robustez` geram resultados idênticos aos da V2 auditada (só o rótulo da V6 muda); 64 testes passam.
- **Testes sem os dados coletados:** os dois testes que conferem a lista de eventos e os lotes horários com os dados reais são pulados num clone sem dados; o teste da regra dos eventos usa um calendário sintético.
- **Decisão (aprovada pelo pesquisador):** adendo 2 ao pré-registro (P1 a P5) e congelamento na tag `congelamento-v2`.

## 2026-11-05 — Documentação em inglês

- **O que entrou:** tradução para o inglês do README, do manual, dos resultados, do pré-registro (com os adendos 1 e 2), do congelamento e da licença dos dados, em `docs/en/` e `LICENSE-DATA.md`.
- **Motivo:** permitir a leitura por pesquisadores de fora do Brasil e preparar artigos.
- **Regras:** o português continua sendo a versão oficial, e cada tradução diz isso no início. Nenhum arquivo congelado foi alterado; os hashes de `congelamento.md` continuam valendo. Gráficos e tabelas automáticas ficam em português, porque são gerados pelo código congelado.
- **Fica só em português:** este diário, `resultados_tabelas.md` e os relatórios das auditorias.

## 2026-11-07 — Conferência dos eventos e painel público

**Conferência por amostragem (pelo pesquisador, 01/11/2026)**
- **O que foi conferido:** 17 eventos de nov/2020 a nov/2022 (relatórios bimestrais, PLDO, PLOA, teto/Auxílio Brasil e PEC da Transição), com a data efetiva de publicação.
- **Resultado:** todas as datas agendadas bateram com a regra do prazo legal. Quando o dia 22 cai no fim de semana, o relatório sai na sexta anterior, o que a janela de −1 a +3 já cobre.
- **Única divergência:** a fala de Guedes sobre a "licença para gastar" foi em 20/10/2021, à tarde, depois da janela da PTAX. A data do evento continua 21/10/2021, primeiro dia em que a janela pode reagir.
- **O que não muda:** na versão congelada, a coluna `data_anuncio` desse evento ficou com 21/10/2021. Essa coluna não entra em nenhum cálculo (só num teste de consistência), então nenhum resultado muda. Para não alterar arquivos congelados (`eventos.csv` e `montar_eventos.py`, com hash em `congelamento.md`), a correção fica registrada só aqui.
- **Por que só agora:** o registro foi feito em 01/11/2026 na branch `eventos-fechados`, que não chegou a virar PR. `resultados.md` (seção 7) e `manual.md` já citavam a conferência; este diário ainda dizia "pendente". A branch pode ser apagada.

**Painel público (repositório `agio-painel`)**
- **O que é:** página estática no GitHub Pages com o nível diário do ágio, na janela da PTAX e no fechamento, atualizada toda semana.
- **Como lê os dados:** um script no repositório do painel lê `dados/tratado/agio_diario.csv` e `agio_fechamento_diario.csv`, gravados por `agio calcular` na coleta semanal. Nenhum arquivo deste repositório muda.
- **Exposição:** o painel mostra o nível do ágio também nos dias da amostra de validação (a partir de 02/11/2026). Não mostra regressões, estudos de evento nem decisões sobre as hipóteses. Nenhum comando de análise roda sobre a validação fora das datas do pré-registro (out/2027 descritiva e out/2028 decisão).
- **Por que registrar:** ver o nível do ágio não muda nenhuma regra fixada, mas a exposição a dados novos deve ficar documentada, como em `congelamento.md`.

## 2026-11-07 — Eventos agendados até 2027 (validação)

- **O que entrou em `scripts/montar_eventos.py`:**
  - **Copom:** decisões de 04/11/2026 e 09/12/2026 e as oito reuniões de 2027 (27/01, 17/03, 28/04, 16/06, 04/08, 22/09, 27/10 e 08/12), pelo calendário que o Banco Central divulgou em 23/06/2026.
  - **Fed:** decisão de 09/12/2026 e as oito reuniões de 2027 (27/01, 17/03, 28/04, 09/06, 28/07, 15/09, 27/10 e 08/12), pelo calendário do Fed. As datas são provisórias até a reunião anterior; mudanças entram aqui com data e motivo.
  - **Fiscais por regra:** PLDO 2028, PLOA 2028 e os relatórios bimestrais de 2027, pelo mesmo prazo legal usado na descoberta.
- **Por quê:** o adendo 2 (P4) prevê a inclusão dos calendários da validação pela mesma regra. É inclusão de dados prevista, não mudança de método.
- **O que não muda:** `FIM_DADOS` continua em 30/10/2026, então `dados/manual/eventos.csv` (158 eventos) não muda e o hash dele em `congelamento.md` continua valendo. Conferido: o script antigo e o novo geram a mesma lista; 62 testes passam e 2 são pulados num clone sem dados.
- **Hash novo do script:** `montar_eventos.py` passa a ter SHA-256 `34c1a45cd5747c70ff242cafc98bef2690eb21da4a07f2d59fb6809d551f5e5d` (antes `c3926d7f…`). Registrado em `congelamento.md`.
- **Prévia da validação de 2027 (até 29/10/2027):** 24 eventos agendados (9 Copom, 8 Fed e 7 fiscais), antes dos não agendados. Domésticos (fiscais e políticos) ficam abaixo de 10, como o adendo 2 já previa para a leitura de 2027.
- **Pendente para o fechamento da lista (out/2027):** decidir, antes de rodar o teste, como gerar a lista da validação sem mudar a da descoberta. Ao estender `FIM_DADOS`, eventos do fim de out/2026 podem passar a contar como sobrepostos a eventos de nov/2026. Opção natural: um arquivo próprio para a validação (por exemplo, `eventos_validacao.csv`), deixando `eventos.csv` como está. A decisão entra aqui antes de qualquer análise.

## 2026-11-07 — Como a lista da validação entra (aprovado pelo pesquisador)

- **Problema:** ao estender `FIM_DADOS`, eventos do fim de out/2026 podem passar a contar como sobrepostos a eventos de nov/2026, o que mudaria a lista da descoberta.
- **Proposta descartada:** um arquivo próprio para a validação (`eventos_validacao.csv`), sugerido no registro anterior. `agio testar` só lê `dados/manual/eventos.csv` e recorta por `--inicio` e `--fim`; ler outro arquivo exigiria mudar `src/agio/cli.py`, que está congelado.
- **Decisão:** `eventos.csv` só cresce por acréscimo no fim.
  - As 158 linhas da descoberta ficam idênticas às da tag `congelamento-v2`, inclusive a coluna `sobreposto`.
  - As linhas da validação entram depois delas. A sobreposição de cada nova linha considera todos os eventos, inclusive os de out/2026 cuja janela alcança novembro.
  - Um teste confere que as 158 primeiras linhas continuam iguais às da tag.
  - Nenhum código congelado muda; o recorte por datas do `testar` já separa as amostras.
- **Efeito colateral aceito:** `agio testar` sem datas passa a misturar descoberta e validação. Os resultados da descoberta ficam na tag `congelamento-v2` e em `resultados.md`.
- **Quando:** a implementação entra no fechamento da lista de 2027 (até 15/09/2027, com os não agendados até 29/10/2027), sempre antes de qualquer análise da validação.

## 2026-11-10 — Licença dos dados: CC BY 4.0 → CC BY-NC-SA 4.0

- **O que muda:** os dados derivados de `dados/tratado/` passam de CC BY 4.0 para CC BY-NC-SA 4.0 (`LICENSE-DADOS.md`, `LICENSE-DATA.md`, READMEs e manuais). O código continua sob MIT.
- **Por quê:** os termos de uso do Binance Vision pedem que dados derivados dos seus conjuntos de dados sejam redistribuídos sob CC BY-NC-SA 4.0. O projeto usa a API pública de mercado (`data-api.binance.vision`), e não está claro se esses termos se aplicam a ela; por prudência, a licença segue a mais restritiva. O painel público (`agio-painel`) já usava a mesma licença.
- **Efeito:** nenhum para o TCC, artigos ou uso acadêmico. Uso comercial passa a depender de autorização. As séries não estão versionadas no GitHub (`dados/tratado/` só tem `.gitkeep`); a licença vale para quando forem distribuídas.
- **Congelamento:** nenhum arquivo com hash em `congelamento.md` muda.

## 2026-11-10 — Mercado Bitcoin bloqueado; validação segue com a Binance

- **O que aconteceu:** a API pública do Mercado Bitcoin (`api.mercadobitcoin.net/api/v4/candles`) passou a responder 403. A resposta é a página "Attention Required! | Cloudflare", ou seja, um bloqueio do serviço de proteção da corretora. O bloqueio aparece também em outra rede (5G de celular) e pelo navegador; não é do IP do pesquisador nem do programa.
- **Desde quando:** primeira falha na coleta de 02/11/2026 (a primeira da validação), repetida em 09/11 e 10/11/2026. Os dias da descoberta, até 30/10/2026, ficaram com as duas corretoras (`n_fontes` = 2).
- **O que o programa faz:** segue com as fontes que respondem, como já previsto no código. Os dias da validação ficam com o ágio só da Binance (`n_fontes` = 1).
- **Efeito medido na descoberta** (dias com as duas corretoras, 11/03/2023 a 30/10/2026, 914 dias): correlação de 0,999 entre o ágio consolidado e o só da Binance; diferença média de −0,004 p.p. (mediana 0,000); em 95% dos dias a diferença absoluta fica abaixo de 0,028 p.p.; máximo de 0,18 p.p. Antes de 11/03/2023 o indicador já era só da Binance, e a robustez da descoberta ("5. Só binance") manteve os resultados do dólar e do VIX.
- **Decisão:** nenhuma série é trocada e nenhum método muda, então não há adendo (pré-registro, "Coleta durante a validação" e P4). A mudança de composição fica registrada aqui e entra como limitação no texto.
- **Acompanhamento:** a coleta continua tentando o Mercado Bitcoin toda semana. Se voltar, os dias recuperados entram normalmente e isso é registrado aqui. Não haverá tentativa de contornar o bloqueio (proxy ou troca de identificação).

