# Resultados: Medo fiscal ou medo global? O ágio da stablecoin em reais diante de choques domésticos e externos (2020–2026)

*Registro completo dos testes e verificações da amostra de descoberta (13/10/2020 a 30/10/2026), na ordem em que foram feitos. Números das tabelas: `resultados_tabelas.md`, gerado por `agio relatorio`. Decisões e motivos: `decisoes.md`. Validação fora da amostra: `pre-registro.md`.*

## Resumo

| Pergunta | Resposta na descoberta | Situação |
| --- | --- | --- |
| O estresse fiscal (juro real de 10 anos) eleva o ágio? | Não: efeito pequeno, só a 10% (p = 0,088), e frágil na robustez | Hipótese original **não confirmada**; repetida na validação (V1) |
| Anúncios domésticos elevam o ágio mais que choques externos? | Não na lista completa (p = 0,77) | **Não confirmada** |
| Crises elevam a participação no mercado? | Não mais que em dias sorteados (p = 0,63) | Hipótese comportamental **não confirmada**; repetida (V2) |
| O medo global (VIX) eleva o ágio? | Sim, robusto (7 de 9 especificações) | Exploratória; confirmação na validação (V3) |
| O câmbio oficial passa para o USDT por inteiro no dia? | Não: o ágio cai 0,13 p.p. a cada 1% de alta do dólar | Exploratória; confirmação na validação (V4) |

**Conclusão provisória:** o ágio do USDT em reais não funciona como termômetro do estresse fiscal brasileiro. Ele é movido pelo câmbio oficial, que o USDT acompanha só em parte no mesmo dia, e pelo medo global.

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
| Liquidez na janela | 3 horas com negócio todos os dias; volume 52% maior (R$ 17,1 mi → R$ 26,1 mi) | Não é preço de poucos negócios |
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
- **VIX:** um salto de 10 pontos eleva o ágio em cerca de 0,2 p.p. no dia e 0,15 p.p. no dia seguinte.
- **Participação:** o número de negócios anormal não responde ao juro nem ao VIX. O ticket médio cai quando o dólar sobe (p = 0,044).

## 6. Robustez (Figura 8)

O teste repete a regressão em 9 especificações: winsorizada, Huber, ágio de fechamento, cada corretora separada, antes e depois de 04/05/2026, e janela até 14h.

- **VIX do dia anterior:** significativo em 7 de 9. As duas exceções têm poucos dados: Mercado Bitcoin, com 884 dias, e o período pós-04/05/2026, com 127 dias.
- **Juro real:** nunca positivo e significativo a 5%. Com a janela até 14h, cai para 0,0006 (p = 0,59). No ágio de fechamento sai negativo, o que reflete o problema de horário.
- **Dólar:** negativo e forte em todas as especificações alinhadas à PTAX.

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
| Sem sobrepostos (62 eventos) | −0,265 (0,30) | +0,80 no ágio ajustado (0,033) | +0,67 (0,35) |

- **Teste t contra teste de permutação.** O número de negócios parece subir nos eventos pelo teste t (p = 0,001), mas sobe igual nos dias sorteados, porque o mercado cresceu no período. A comparação válida é a de permutação.
- **Sem os eventos sobrepostos,** os choques externos isolados *reduzem* o ágio ajustado em 0,61 p.p. (p = 0,035). É daí que vem a diferença entre domésticos e externos, já que os domésticos ficam perto de zero.
- **Cuidado com testes múltiplos.** Foram cerca de 40 testes, e ao nível de 5% se esperam cerca de 2 significativos só por acaso. O resultado dos externos isolados é exploratório (V5 no pré-registro).

## 8. Aplicação da regra de decisão

| Hipótese | Condição | Resultado |
| --- | --- | --- |
| Original | Juro real > 0, p < 5% | Não (p = 0,088) |
| | e domésticos > externos | Não na lista completa; só sem sobrepostos, e porque os externos são negativos |
| Comportamental | Participação nas crises > dias sorteados | Não (p = 0,63) |

As duas hipóteses do TCC não se confirmam na amostra de descoberta.

## 9. Limitações

- **Dados agregados:** medem comportamento coletivo, não a motivação de cada investidor.
- **Peso da Binance:** o indicador é, na prática, o de uma corretora.
- **Proxy do estresse fiscal:** o juro real de 10 anos é uma medida indireta; o CDS ficou de fora por custo.
- **Horário do VIX:** o VIX fecha depois da janela da PTAX. Por isso o resultado mais limpo é o do dia anterior.
- **Pouco tempo depois da regulação:** 127 dias, sem poder estatístico.
- **Google Trends ainda não importado:** os sinais de busca ficam para a próxima rodada.
- **Testes múltiplos:** ver a seção 7.
- **Episódio de jun–jul/2026:** causa não identificada; a escassez global de USDT foi testada e não se confirmou.

## 10. Próximos passos

1. **Validação fora da amostra** (`pre-registro.md`): análise intermediária em 30/10/2027 e final em 31/10/2028.
2. **Episódio de jun–jul/2026:** fenômeno de mercado confirmado; escassez global de USDT descartada (seção 3.1). A causa fica em aberto para o mestrado.
3. **Google Trends:** importar os CSVs e repetir a análise comportamental.
4. **Ponte para o mestrado:** repasse incompleto do câmbio e medo global, se confirmados na validação.

## Registro de erros encontrados e corrigidos

| Data | Erro | Correção |
| --- | --- | --- |
| 31/10/2026 | Ágio de fechamento distorcido em dias de choque (horário) | Medida alinhada à janela da PTAX |
| 31/10/2026 | FRED fora do ar na coleta do VIX | Alternativa da Cboe; coleta mais curta |
| 01/11/2026 | Lista de eventos escolhida à mão, depois de ver os dados | Regra fixa, gerada por script |
| 01/11/2026 | Pausa das tarifas datada no dia do anúncio (14h, depois da janela) | 10/04/2025 |
| 01/11/2026 | 04/05/2026 tratado como início efetivo da obrigação de reporte | Registrado como início previsto; adiamento (Res. 574) entra como evento |
| 01/11/2026 | Exclusão do placebo de 10 dias esgotaria o sorteio com 158 eventos | 4 dias úteis (janelas não se cruzam) |

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
