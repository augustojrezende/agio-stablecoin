# Resultados: O ágio da stablecoin em reais: reação a choques domésticos e externos no Brasil (2020–2026)

*Registro completo dos testes e verificações da amostra de descoberta (13/10/2020 a 30/10/2026), na ordem em que foram feitos. Números das tabelas: `resultados_tabelas.md`, gerado por `agio relatorio`. Decisões e motivos: `decisoes.md`. Validação fora da amostra: `pre-registro.md`. Atualizado em 05/11/2026 com as correções das auditorias AUD-001 a AUD-003 (seção 11); os números deste arquivo são os da versão corrigida.*

## Resumo

| Pergunta | Resposta na descoberta | Situação |
| --- | --- | --- |
| O estresse fiscal (juro real de 10 anos) eleva o ágio? | Não: efeito pequeno, só a 10% (p = 0,088), e frágil na robustez | Hipótese original **não confirmada**; repetida na validação (V1) |
| Anúncios domésticos elevam o ágio mais que choques externos? | Não na lista completa (p = 0,77) | **Não confirmada** |
| Crises elevam a participação no mercado? | Não mais que em dias sorteados (p = 0,63) | Hipótese comportamental **não confirmada**; repetida (V2) |
| O medo global (VIX) está associado a ágio maior? | Sim: positivo em 7 de 9 especificações, mas concentrado em 2020–2022 e sensível a poucos dias | Exploratória; confirmação na validação (V3) |
| O câmbio oficial passa para o USDT por inteiro no dia? | Não: o preço do USDT acompanha cerca de 86% da variação da PTAX; o ágio cai 0,13 p.p. a cada 1% de alta | Exploratória; confirmação na validação (V4a) |
| O ágio volta nos dias seguintes? | Não: continua caindo por mais 2 dias (total de cerca de −0,21 p.p. por 1%) | Contrário à V4b; nova V6, persistência negativa (adendo ao pré-registro); mecanismo não identificado |

**Conclusão provisória:** o ágio do USDT em reais não se comportou como termômetro do estresse fiscal brasileiro medido pelo juro real, o que não prova que o risco fiscal seja irrelevante. As associações mais claras são com o câmbio oficial, que o USDT acompanha só em parte no mesmo dia, e com o medo global. São associações observadas, não relações de causa.

## 1. Dados e cobertura

- **Fontes, todas gratuitas:** PTAX de venda (Banco Central, Olinda); candles diários e horários do USDT/BRL (Binance desde 13/10/2020, Mercado Bitcoin desde 11/03/2023); juro real de 10 anos (Tesouro IPCA+, taxa da manhã, interpolada); VIX (Cboe, porque o FRED ficou fora do ar).
- **Cobertura:** 1.520 dias úteis com ágio; 1.490 entram nas regressões, porque o ágio anormal precisa de pelo menos 30 dias de histórico.
- **Ágio normal:** cerca de 1% em 2020, caindo para 0,2–0,3% em 2025–26 (Figura 1).

## 2. Verificação: o horário de medição

**Problema encontrado:** na primeira coleta, os menores ágios da série caíam justamente nos dias de choque: 09/04/2025 com −3,5%, 26/10/2026 com −2,1% e 06/11/2024 com −1,8%. A causa era o horário. A PTAX é formada entre 10h e 13h, e o candle diário das corretoras fecha às 21h.

**Correção:** a medida principal passou a usar o preço do USDT ponderado pelo volume entre 10h e 13h de Brasília.

**Resultado da verificação:**
- 09/04/2025 passou de −3,5% para cerca de 0%;
- a correlação entre as duas medidas é 0,54 (Figura 2);
- o desvio padrão de 2025 caiu de 0,53 para 0,19 p.p.

**Custo:** a correlação entre corretoras caiu de 0,91 para 0,68, porque há menos negócios em 3 horas (Figura 3). O indicador consolidado é, na prática, o da Binance, que concentra o volume.

## 3. Análise descritiva

- **Choques domésticos não elevaram o ágio.** Pacote fiscal (29/11/2024): −1,5 p.p. de ágio anormal. Segundo turno (26/10/2026): −0,8 p.p.
- **O maior ágio anormal da série foi externo.** Em 05/08/2024 (turbulência global), +3,0 p.p. (Figura 4).
- **A participação disparou nos grandes choques.** O número de negócios dobrou ou triplicou, e o ticket médio caiu.
- **Episódio sem explicação.** De 24/06 a meados de julho de 2026, o ágio ficou entre 1% e 1,7%. Diagnóstico na seção 3.1.

### 3.1 Episódio de ágio alto (24/06 a meados de julho de 2026)

*Diagnóstico com `agio episodio --inicio 2026-06-01 --fim 2026-08-15`, comparando o período com os 90 dias anteriores. Gráfico: `figuras/episodio_20260601_20260815.png`.*

| Verificação | Resultado | Leitura |
| --- | --- | --- |
| Duas corretoras? | Sim: correlação de 0,83 no episódio; média de +0,50 p.p. na Binance e +0,35 p.p. no Mercado Bitcoin (antes: 0,07 e 0,01) | Fenômeno de mercado, não de uma corretora |
| Janela e fechamento? | Os dois sobem juntos (fechamento: 0,17 → 0,67 p.p.) | Nível do preço, não horário |
| Liquidez na janela | 3 horas com negócio todos os dias; volume 52% maior (17,1 mi → 26,1 mi de USDT) | Não é preço de poucos negócios |
| De que lado veio? | A PTAX ficou em R$ 5,17–5,21 e o USDT subiu até R$ 5,28; depois a PTAX caiu e o USDT acompanhou devagar | O USDT ficou caro, e a diferença levou cerca de 4 semanas para fechar |
| Quem comprou? | Ticket médio 39% maior (R$ 6,5 mil → R$ 9,0 mil); número de negócios igual; pressão compradora menor (0,55 → 0,51) | Operações maiores, sem pressa de compra; não é corrida do varejo |

- **Conclusão do diagnóstico:** o episódio é real, não é erro de medição.
- **O sinal contrariou o efeito mecânico.** No primeiro dia (24/06), o dólar subiu 0,69%, o que pelo efeito mecânico reduziria o ágio, e mesmo assim o ágio saltou para 1,5%.
- **Padrão compatível com falta de vendedores**, mais do que com excesso de compradores: preço alto sem urgência na compra e convergência lenta. Em outras palavras, a arbitragem ficou lenta por algumas semanas.
- **Hipótese testada (exploratória):** escassez de USDT. Em junho de 2026 a oferta global de stablecoins teve a maior contração mensal desde 2022, e o USDT caiu de cerca de US$ 190 bi para US$ 184 bi.
- **Outro fator possível:** aversão a risco no próprio dia 24/06 (ouro −3,4%, Ibovespa −0,4%).
- **Descartados pelo noticiário como causa única:** Resolução 574 (18/06), IOF sobre stablecoins (sem decreto), Resolução 561 (vigência só em 01/10) e saída de corretoras menores. Detalhes e fontes em `decisoes.md`.
- **Teste exploratório, fora do pré-registro (`agio oferta-usdt`):** a regressão do ágio anormal ganhou mais uma variável, a variação de 5 dias da oferta global de USDT (DefiLlama), com 1 dia de defasagem.

| Variável | Coeficiente | p-valor |
| --- | --- | --- |
| Variação da oferta de USDT (5 dias, %) | +0,031 | 0,051 |
| Variação do dólar oficial (%) | −0,128 | < 0,001 |
| Variação do juro real 10 anos (bp) | +0,0018 | 0,118 |
| Variação do VIX no dia | +0,022 | 0,045 |
| Variação do VIX no dia anterior | +0,016 | 0,008 |

  - **A hipótese da escassez não se confirma.** O sinal é positivo, o contrário do previsto, e não chega a 5%.
  - **A sequência mensal confirma:** a oferta caiu de maio a julho (US$ 188,4 bi para 183,5 bi) e caiu ainda mais em outubro (180,1 bi), sem novo salto do ágio.
  - **Leitura do sinal positivo:** a oferta parece acompanhar a demanda global. Quando a procura sobe, a Tether emite mais, e o ágio sobe junto.
  - **Ganho lateral de robustez:** com a variável a mais, o VIX e o dólar não mudam.
- **Conclusão sobre o episódio:** é um fenômeno de mercado real, e a causa continua não identificada. A escassez global foi testada e descartada. O mais provável é um atrito local na arbitragem entre o câmbio oficial e o mercado de USDT no Brasil, que os dados disponíveis não medem. Fica como pergunta para o mestrado (limites à arbitragem).

## 4. Desenho do teste formal (fixado antes de rodar)

- **Regressão com todos os dias.** Variável dependente: ágio anormal. Variáveis explicativas: variação do dólar oficial, do juro real de 10 anos (em bp), do VIX no dia e no dia anterior, e o tamanho do mercado. Estimação por MQO, com erros de Newey-West.
- **Estudo de evento.** Janela de −1 a +3 dias úteis. Teste t e teste de permutação contra datas sorteadas. Comparação de choques domésticos com externos.
- **Regra de decisão.**
  - A hipótese original se confirma se o juro real tiver coeficiente positivo e significativo a 5% **e** os choques domésticos tiverem ágio maior que os externos.
  - A versão comportamental se confirma se a participação for significativamente maior nas crises.

## 5. Regressões

**Ágio anormal** (1.490 dias):

| Variável | Coeficiente | p-valor |
| --- | --- | --- |
| Variação do dólar oficial (%) | −0,129 | < 0,001 |
| Variação do juro real 10 anos (bp) | +0,0019 | 0,088 |
| Variação do VIX no dia | +0,021 | 0,047 |
| Variação do VIX no dia anterior | +0,016 | 0,008 |
| Tamanho do mercado (log) | +0,029 | 0,087 |

R² = 0,095; curtose dos resíduos = 15,3.

- **Juro real:** um choque fiscal forte, de +20 bp, move o ágio em cerca de 0,04 p.p.
- **VIX:** um salto de 10 pontos está associado a ágio cerca de 0,2 p.p. maior no dia e 0,15 p.p. no dia seguinte.
- **Participação:** o número de negócios anormal não responde ao juro nem ao VIX. O ticket médio cai quando o dólar sobe (p = 0,044).

### 5.1 Repasse do câmbio nos dias seguintes

A regressão de repasse acrescenta a variação do dólar de 1, 2 e 3 dias antes:

| Variável | Coeficiente | p-valor |
| --- | --- | --- |
| Dólar no dia | −0,126 | < 0,001 |
| Dólar 1 dia antes | −0,057 | < 0,001 |
| Dólar 2 dias antes | −0,025 | 0,007 |
| Dólar 3 dias antes | +0,002 | 0,85 |
| Soma das defasagens | −0,080 | < 0,001 |

- **A previsão registrada (V4b) não se confirma.** Ela dizia que o ágio voltaria nos dias seguintes, porque o USDT alcançaria o dólar com atraso. O ágio continua caindo por mais dois dias, e o efeito total chega a cerca de −0,21 p.p. por 1% de alta.
- **Leituras possíveis, não testadas.** Uma é a realização de ganhos (quem tem USDT vende ao longo de alguns dias depois da alta do dólar). Outras são ordens de venda que se ajustam devagar, arbitragem com atraso ou estoque das mesas de liquidez. Os dados agregados não distinguem entre elas.
- **Cuidado com a parte mecânica.** Como ágio = preço do USDT / PTAX − 1, se o USDT reage menos que a PTAX o ágio cai por construção. Com os mesmos controles, o retorno do USDT tem coeficiente 0,856 sobre o dólar (AUD-001): o repasse no dia é de cerca de 86%. A persistência nas defasagens não é identidade contábil, mas também não revela o motivo.
- **Como fica no pré-registro.** Entrou como V6 no adendo 1, para ser confirmada na validação. A V4b continua sendo testada como foi escrita.

### 5.2 Verificação: dias extremos do dólar

O gráfico do dólar (Figura 5) mostrou variações diárias atípicas. Todas foram conferidas:

| Data | Variação do dólar | Intervalo até o dia anterior | O que foi |
| --- | --- | --- | --- |
| 26/10/2026 | +8,8% | fim de semana | Dia seguinte ao segundo turno: dólar +8,21% e Bolsa −13,88% no noticiário |
| 05/10/2026 | −4,7% | fim de semana | Dia seguinte ao primeiro turno de 2026 |
| 09/11/2020 | −4,6% | fim de semana | Fora da regressão (ainda sem histórico para o ágio anormal) |
| 03/10/2022 | −3,9% | fim de semana | Dia seguinte ao primeiro turno de 2022 |

- **São dados reais, não buracos nos dados.**
- **O maior choque doméstico da série** (26/10/2026) teve ágio anormal *negativo* (−0,77 p.p.), coerente com o efeito mecânico do dólar e contrário à hipótese fiscal.
- **Os resultados não dependem desses dias:** a regressão robusta (Huber) e a winsorizada mantêm os sinais (seção 6).

## 6. Robustez (Figura 8)

O teste repete a regressão em 9 especificações: winsorizada, Huber, ágio de fechamento, cada corretora separada, antes e depois de 04/05/2026, e janela até 14h.

- **VIX do dia anterior:** significativo em 7 de 9. As duas exceções têm poucos dados: Mercado Bitcoin, com 884 dias, e o período pós-04/05/2026, com 127 dias.
- **Juro real:** nunca positivo e significativo a 5%. Com a janela até 14h, cai para 0,0006 (p = 0,59). No ágio de fechamento sai negativo, o que reflete o problema de horário.
- **Dólar:** negativo em todas as especificações; significativo em todas, exceto depois de 04/05/2026 (p = 0,111, 127 dias).
- **Sensibilidade do VIX (AUD-001):** com HAC de 10 e 20 defasagens, p = 0,005 e 0,004. Sem os 5 dias de maior influência (o maior é 05/08/2024), o coeficiente cai para 0,006 (p = 0,10); sem 15, 0,008 (p = 0,02). Por subperíodo: 0,025 em 2020–2022 e 0,003 em 2025–2026. A associação existe, mas é concentrada no início da amostra.

## 7. Lista de eventos e estudo de evento (Figuras 6 e 7)

**Problema:** a lista provisória tinha 15 eventos, escolhidos um a um depois de ver os dados.

**Correção:** passou a valer uma regra fixa (`scripts/montar_eventos.py`), que gera 158 eventos com fonte:
- todas as decisões do Copom e do Fed;
- PLDO, PLOA e relatórios bimestrais;
- 5 anúncios fiscais;
- eleições;
- choques externos;
- normas do Banco Central sobre criptoativos.

**Verificações da lista:**
- **Pelo pesquisador:** 17 datas de nov/2020 a nov/2022 conferidas com a publicação efetiva. Todas bateram, exceto o horário da fala de Guedes (20/10/2021, à tarde), o que não muda a data do evento.
- **Na própria lista provisória, dois erros:**
  - a pausa das tarifas foi anunciada às 14h de 09/04/2025, então o evento passa para 10/04;
  - o reporte de cripto no câmbio previsto para 04/05/2026 foi adiado para 03/11/2026 pela Resolução 574.

**Resultados:**

| Lista | Ágio anormal: todos (p perm.) | Domésticos − externos (p perm.) | Negócios: todos (p perm.) |
| --- | --- | --- | --- |
| Completa (154 eventos) | −0,175 (0,36) | +0,07 (0,77) | +0,43 (0,63) |
| Sem sobrepostos (60 eventos) | −0,300 (0,20) | +0,85 no ágio ajustado (0,031) | +0,59 (0,57) |

- **Teste t contra teste de permutação.** O número de negócios parece subir nos eventos pelo teste t (p = 0,001), mas sobe igual nos dias sorteados, porque o mercado cresceu no período. A comparação válida é a de permutação.
- **Correção da auditoria:** o calendário das sobreposições não tinha o feriado de Finados. Com o calendário da PTAX, Copom 28/10/2021 e Fed 04/11/2021 passam a sobrepostos, e a lista isolada cai de 62 para 60 eventos (32 domésticos, 14 externos, 14 monetários). A lista completa não muda.
- **Sem os eventos sobrepostos,** os choques externos isolados ficam associados a ágio ajustado *menor*: −0,67 p.p. (p = 0,024, 14 eventos). É daí que vem a diferença entre domésticos e externos (+0,85, p = 0,031), já que os domésticos ficam perto de zero.
- **A diferença não resiste a placebos temporais.** Embaralhando os rótulos só dentro de cada ano, p = 0,091 (ajustado) e 0,135 (anormal); deslocando as séries dentro de cada ano, p = 0,086 e 0,107. O p = 0,03 depende de comparar eventos de anos diferentes. Leitura correta: diferença nominal, sensível ao desenho do placebo.
- **Cuidado com testes múltiplos.** Foram cerca de 40 testes, e ao nível de 5% se esperam cerca de 2 significativos só por acaso. O resultado dos externos isolados é exploratório (V5 no pré-registro) e não resiste à correção de Holm (p ajustado = 0,072). V3 (0,031), V4a (< 0,001) e V6 (0,002) resistem, o que na descoberta não é confirmação.
- **O rótulo de origem não é sorteado.** 47 dos 53 externos são decisões agendadas do Fed, e os domésticos são quase todos relatórios fiscais agendados. A permutação compara grupos, não mede efeito causal da origem do choque.

### 7.1 Atenção do público (Google Trends), exploratório

*`agio buscas`: buscas anormais = log(1 + interesse) menos a mediana dos 60 dias úteis anteriores. Fora do pré-registro; só a amostra de descoberta. Figuras 9a e 9b (`figuras/09_buscas_dolar.png`, `figuras/09_buscas_usdt.png`).*

| Tipo de evento | Buscas por "dólar" (p perm.) | Buscas por "USDT" (p perm.) |
| --- | --- | --- |
| Externo (53) | +0,38 (0,013) | +0,43 (0,62) |
| Político (4) | +3,01 (< 0,001) | +1,12 (0,64) |
| Fiscal (46) | +0,07 (0,92) | +0,32 (0,48) |
| Monetário (47) | +0,21 (0,26) | +0,32 (0,48) |
| Todos (154) | +0,30 (0,002) | +0,38 (0,29) |
| Não agendados (13) | +1,12 (< 0,001) | +0,88 (0,78) |

- **A atenção ao dólar reage a choques externos e políticos, não aos fiscais.** Nos choques externos, as buscas saltam no dia do evento e saem da faixa das datas sorteadas. Nos anúncios fiscais, ficam dentro dela.
- **As buscas por USDT não reagem aos eventos.** Como o número de negócios, elas crescem com o tempo em qualquer dia.
- **As buscas não antecipam o ágio.** Na regressão com as buscas do dia anterior: USDT +0,067 (p = 0,13) e dólar −0,061 (p = 0,21). Dólar e VIX não mudam.
- **Leitura:** o público presta atenção ao dólar nas eleições e nos choques externos, mas anúncios fiscais nem chegam a chamar a atenção; e atenção alta não vira procura por dólar digital nem ágio.
- **Cuidados:** o grupo político tem 4 eventos (efeito forte, poucos casos); são mais cerca de 12 testes, então a análise ilustra e não confirma.

## 8. Aplicação da regra de decisão

| Hipótese | Condição | Resultado |
| --- | --- | --- |
| Original | Juro real > 0, p < 5% | Não (p = 0,088) |
| | e domésticos > externos | Não na lista completa (p = 0,77); a regra usa a lista completa |
| Comportamental | Participação nas crises > dias sorteados | Não (p = 0,63) |

As duas hipóteses do TCC não se confirmam na amostra de descoberta.

## 9. Limitações

- **Dados agregados:** medem comportamento coletivo, não a motivação de cada investidor.
- **Peso da Binance:** o indicador é, na prática, o de uma corretora.
- **Proxy do estresse fiscal:** o juro real de 10 anos é uma medida indireta; o CDS ficou de fora por custo.
- **Horário do VIX:** o VIX fecha depois da janela da PTAX. Por isso o resultado mais limpo é o do dia anterior.
- **Pouco tempo depois da regulação:** 127 dias, sem poder estatístico.
- **Repasse e identidade:** a PTAX está no denominador do ágio; parte da relação com o dólar é mecânica (seção 5.1).
- **Estudo de evento:** a permutação não reproduz um sorteio da origem dos choques, e o contraste dos isolados depende do placebo (seção 7).
- **Testes múltiplos:** ver a seção 7.
- **Episódio de jun–jul/2026:** causa não identificada; a escassez global de USDT foi testada e não se confirmou.

## 10. Próximos passos

1. **Validação fora da amostra** (`pre-registro.md`, adendo 2): leitura descritiva com dados até 29/10/2027 e decisão única com dados até 31/10/2028.
2. **Episódio de jun–jul/2026:** fenômeno de mercado confirmado; escassez global de USDT descartada (seção 3.1). A causa fica em aberto para o mestrado.
3. **Ponte para o mestrado:** repasse incompleto do câmbio e medo global, se confirmados na validação.

## Registro de erros encontrados e corrigidos

| Data | Erro | Correção |
| --- | --- | --- |
| 31/10/2026 | Ágio de fechamento distorcido em dias de choque (horário) | Medida alinhada à janela da PTAX |
| 31/10/2026 | FRED fora do ar na coleta do VIX | Alternativa da Cboe; coleta mais curta |
| 01/11/2026 | Lista de eventos escolhida à mão, depois de ver os dados | Regra fixa, gerada por script |
| 01/11/2026 | Pausa das tarifas datada no dia do anúncio (14h, depois da janela) | 10/04/2025 |
| 01/11/2026 | 04/05/2026 tratado como início efetivo da obrigação de reporte | Registrado como início previsto; adiamento (Res. 574) entra como evento |
| 01/11/2026 | Exclusão do placebo de 10 dias esgotaria o sorteio com 158 eventos | 4 dias úteis (janelas não se cruzam) |
| 02/11/2026 | `agio robustez` falhava com índices duplicados ao juntar lotes (AUD-001-06) | Índice novo e remoção de duplicatas; 9 especificações iguais |
| 02/11/2026 | Calendário das sobreposições sem feriados (AUD-001-10) | Calendário da PTAX; 62 → 60 isolados |
| 02/11/2026 | V1 sem mínimo de eventos (AUD-001-21) | Mínimo de 10 por grupo, senão inconclusivo |
| 02/11/2026 | Família de Holm encolhia sem a V5 (AUD-001-22) | Sete posições sempre |
| 02/11/2026 | Mediana da Figura 1 incluía o próprio dia (AUD-001-26) | Mesma mediana do indicador |
| 02/11/2026 | Trajetórias mostravam n nominal (AUD-001-27) | n válido por dia |
| 02/11/2026 | Volume do episódio rotulado em reais (AUD-001-31) | USDT |

## 11. Auditoria independente (AUD-001 a AUD-003)

Três auditorias revisaram o projeto em 02/11/2026: diagnóstico (AUD-001), correção numa cópia separada (AUD-002) e parecer final (AUD-003). Os relatórios estão em `auditorias/`.

- **Sete erros comprovados, todos corrigidos** (tabela acima). Nenhum mudou a regressão principal, a robustez ou a decisão de qualquer hipótese.
- **Reprodução:** com o código corrigido, `agio testar` e `agio robustez` reproduzem do zero todos os resultados da cópia auditada; 64 testes automatizados.
- **Parecer:** aprovado com ressalvas, como estudo observacional e exploratório. As ressalvas estão nas seções 5.1, 6, 7 e 9.
- **O que mudou nos números:** a lista isolada (seção 7) e o rótulo da V6, que passou a descrever o padrão ("ágio segue caindo após alta do dólar") em vez de um mecanismo.

## Figuras

Geradas por `agio relatorio` em `docs/figuras/`; legendas completas em `resultados_tabelas.md`.

1. Série do ágio (janela da PTAX, fechamento e mediana móvel)
2. Janela da PTAX contra fechamento
3. Ágio por corretora
4. Ágio anormal e choques não agendados
5. Dólar oficial e ágio anormal (repasse incompleto)
6. Trajetória do ágio ajustado em torno dos eventos, contra datas sorteadas
7. Trajetória do número de negócios em torno dos eventos
8. Robustez: coeficientes e intervalos de 95%
