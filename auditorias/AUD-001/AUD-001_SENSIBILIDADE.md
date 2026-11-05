# AUD-001 — Sensibilidade estatística

Todos os testes aqui denominados suplementares pertencem à auditoria. Não substituem especificação, evento, hipótese ou resultado original. Não houve busca de uma especificação significativa. HAC 5/10/20, exclusão dos 1/5/15 maiores Cook e três períodos de calendário foram apresentados integralmente, inclusive resultados contrários. São diagnósticos condicionais aos dados observados; p-valores suplementares não receberam correção global de multiplicidade e não são confirmações novas.

## Regressões: original e HAC suplementar

HAC(5) é original. Todos têm n=1490 e os mesmos coeficientes; apenas a matriz de covariância muda. IC de 95% normal assintótico, Bartlett, sem correção de pequena amostra. Unidades: ágio anormal em p.p.; dólar em 100×retorno log; juro em bp; VIX em pontos; mercado em log do volume mediano anterior.

| teste | variavel | n | coef | ep | p | ic_inf | ic_sup |
|---|---|---|---|---|---|---|---|
| HAC 5 | Intercept | 1490 | -0.52286301 | 0.28928247 | 0.07069246 | -1.0898462 | 0.04412021 |
| HAC 5 | d_dolar | 1490 | -0.12899693 | 0.013453144 | 8.9281465e-22 | -0.1553646 | -0.10262925 |
| HAC 5 | d_juro_bp | 1490 | 0.0019273021 | 0.0011281222 | 0.087559178 | -0.00028377686 | 0.004138381 |
| HAC 5 | d_vix | 1490 | 0.021234987 | 0.010681979 | 0.046819844 | 0.00029869263 | 0.042171282 |
| HAC 5 | d_vix_ant | 1490 | 0.015633966 | 0.0058795128 | 0.0078359438 | 0.004110333 | 0.0271576 |
| HAC 5 | log_mercado | 1490 | 0.029439499 | 0.017189659 | 0.086780911 | -0.004251613 | 0.063130611 |
| HAC 10 | Intercept | 1490 | -0.52286301 | 0.31199044 | 0.093758889 | -1.134353 | 0.08862701 |
| HAC 10 | d_dolar | 1490 | -0.12899693 | 0.013471095 | 1.0104163e-21 | -0.15539979 | -0.10259407 |
| HAC 10 | d_juro_bp | 1490 | 0.0019273021 | 0.0011305999 | 0.088255613 | -0.00028863309 | 0.0041432373 |
| HAC 10 | d_vix | 1490 | 0.021234987 | 0.010646849 | 0.046099008 | 0.00036754681 | 0.042102427 |
| HAC 10 | d_vix_ant | 1490 | 0.015633966 | 0.0055815947 | 0.0050946799 | 0.0046942416 | 0.026573691 |
| HAC 10 | log_mercado | 1490 | 0.029439499 | 0.018711637 | 0.11564342 | -0.0072346348 | 0.066113633 |
| HAC 20 | Intercept | 1490 | -0.52286301 | 0.30364839 | 0.085081166 | -1.1180029 | 0.072276904 |
| HAC 20 | d_dolar | 1490 | -0.12899693 | 0.014593182 | 9.6118566e-19 | -0.15759904 | -0.10039482 |
| HAC 20 | d_juro_bp | 1490 | 0.0019273021 | 0.0011755786 | 0.10111963 | -0.0003767897 | 0.0042313939 |
| HAC 20 | d_vix | 1490 | 0.021234987 | 0.01047554 | 0.042651986 | 0.00070330653 | 0.041766668 |
| HAC 20 | d_vix_ant | 1490 | 0.015633966 | 0.0053967695 | 0.0037685548 | 0.0050564924 | 0.02621144 |
| HAC 20 | log_mercado | 1490 | 0.029439499 | 0.01851221 | 0.11177291 | -0.0068437664 | 0.065722765 |

O dólar continua negativo; VIX contemporâneo e anterior continuam positivos a 5%. Juro continua não significativo a 5%; com HAC20 também ultrapassa 10%. Isso não prova ausência de efeito fiscal. O controle log_mercado perde o limiar de 10% com 10/20 defasagens.

## Influência e estabilidade: somente suplementos

| teste | variavel | n | coef | ep | p | ic_inf | ic_sup |
|---|---|---|---|---|---|---|---|
| Sem 1 maiores Cook | d_dolar | 1489 | -0.1273422 | 0.013320941 | 1.1827027e-21 | -0.15345076 | -0.10123363 |
| Sem 1 maiores Cook | d_juro_bp | 1489 | 0.0022278419 | 0.0010840656 | 0.039871243 | 0.00010311239 | 0.0043525713 |
| Sem 1 maiores Cook | d_vix | 1489 | 0.011164425 | 0.0055057644 | 0.042583713 | 0.00037332474 | 0.021955525 |
| Sem 1 maiores Cook | d_vix_ant | 1489 | 0.011229103 | 0.0043277866 | 0.0094686534 | 0.0027467975 | 0.019711409 |
| Sem 5 maiores Cook | d_dolar | 1485 | -0.11834026 | 0.012345209 | 9.1632022e-22 | -0.14253642 | -0.094144092 |
| Sem 5 maiores Cook | d_juro_bp | 1485 | 0.0014028902 | 0.00098443694 | 0.15413737 | -0.00052657078 | 0.0033323511 |
| Sem 5 maiores Cook | d_vix | 1485 | 0.007992108 | 0.0050382034 | 0.11267101 | -0.0018825893 | 0.017866805 |
| Sem 5 maiores Cook | d_vix_ant | 1485 | 0.0063869115 | 0.0038811695 | 0.099843007 | -0.0012200409 | 0.013993864 |
| Sem 15 maiores Cook | d_dolar | 1475 | -0.10529582 | 0.010346771 | 2.5200124e-24 | -0.12557512 | -0.085016525 |
| Sem 15 maiores Cook | d_juro_bp | 1475 | 0.0015393981 | 0.00087614528 | 0.078915704 | -0.00017781512 | 0.0032566113 |
| Sem 15 maiores Cook | d_vix | 1475 | 0.0066154203 | 0.0047725299 | 0.16570251 | -0.0027385663 | 0.015969407 |
| Sem 15 maiores Cook | d_vix_ant | 1475 | 0.0079340883 | 0.0034674454 | 0.022127894 | 0.0011380203 | 0.014730156 |
| 2020-01-01 a 2023-01-01 exclusivo | d_dolar | 528 | -0.16494991 | 0.022258034 | 1.2553698e-13 | -0.20857485 | -0.12132496 |
| 2020-01-01 a 2023-01-01 exclusivo | d_juro_bp | 528 | 0.0054542836 | 0.0023508006 | 0.020331071 | 0.00084679912 | 0.010061768 |
| 2020-01-01 a 2023-01-01 exclusivo | d_vix | 528 | 0.023643475 | 0.010054106 | 0.018691668 | 0.0039377894 | 0.043349161 |
| 2020-01-01 a 2023-01-01 exclusivo | d_vix_ant | 528 | 0.025106289 | 0.0079971851 | 0.0016929955 | 0.0094320939 | 0.040780484 |
| 2023-01-01 a 2025-01-01 exclusivo | d_dolar | 502 | -0.12261432 | 0.020427548 | 1.9442152e-09 | -0.16265158 | -0.082577062 |
| 2023-01-01 a 2025-01-01 exclusivo | d_juro_bp | 502 | -0.0020705744 | 0.0014830645 | 0.16267058 | -0.0049773274 | 0.00083617869 |
| 2023-01-01 a 2025-01-01 exclusivo | d_vix | 502 | 0.039900577 | 0.034702457 | 0.25022991 | -0.028114989 | 0.10791614 |
| 2023-01-01 a 2025-01-01 exclusivo | d_vix_ant | 502 | 0.016525194 | 0.017576477 | 0.34712111 | -0.017924068 | 0.050974457 |
| 2025-01-01 a 2026-10-31 exclusivo | d_dolar | 460 | -0.059737225 | 0.014212728 | 2.63308e-05 | -0.087593659 | -0.031880791 |
| 2025-01-01 a 2026-10-31 exclusivo | d_juro_bp | 460 | -0.00057024737 | 0.0012919681 | 0.65893876 | -0.0031024583 | 0.0019619636 |
| 2025-01-01 a 2026-10-31 exclusivo | d_vix | 460 | 0.0030075332 | 0.0045124981 | 0.50509818 | -0.0058368004 | 0.011851867 |
| 2025-01-01 a 2026-10-31 exclusivo | d_vix_ant | 460 | 0.002528142 | 0.003745048 | 0.49963597 | -0.0048120173 | 0.0098683013 |

05/08/2024 tem Cook≈0,8155 (influencia.csv). Remover essa observação reduz o coeficiente VIX contemporâneo de 0,02123 para 0,01116; retirar cinco maiores Cook leva VIX anterior a 0,00639 (p=0,09984). Retirar quinze produz p=0,02213: a sensibilidade não é monotônica. Juro passa p=0,03987 ao retirar um caso e p=0,15414 ao retirar cinco: não selecionar uma dessas versões como evidência confirmatória. Exclusão por influência depende da resposta e altera o estimando; a covariância HAC também passa a operar sobre sequência com observações removidas. Preferir ler estes resultados como diagnóstico.

Os três períodos mostram dólar sempre negativo, com magnitude menor no fim; VIX anterior passa de 0,0251 para 0,00253. Diferença de significância entre períodos não é teste de diferença de coeficientes. Não declaramos quebra estrutural. As nove robustezes originais foram recalculadas integralmente em robustez_recalculada_auditoria.csv: diferença máxima zero. Huber não tem HAC. O juro do fechamento é negativo/significativo; o dólar pós-04/05/2026 tem p=0,111, portanto “forte em todas” não deve ser lido como “significativo em todas”.

## Eventos: desenho e resultados lado a lado

Original: 5000 sorteios, semente 42; CAR soma cinco níveis anormais (−1,+3); p bilateral. Datas placebo com reposição e exclusão de ±4 posições de eventos elegíveis da lista fornecida. Rótulos doméstico/externo embaralhados mantendo tamanhos dos grupos. A docstring ainda menciona ±10, mas constante e execução são ±4. CAR é área discreta do prêmio anormal, em p.p. somados ao longo de cinco dias, não retorno acumulado de um ativo.

Suplementos: 5000 sorteios, semente 20261102 (gerador sequencial no script), p=(1+b)/(5001). Não constituem randomização verdadeira dos choques:

1. **Rótulos dentro do ano:** preserva contagem doméstica/externa anual, centra CAR pela média dos eventos do ano e permuta dentro de ano. A estatística centrada difere da diferença bruta porque controla composição anual. Ainda não resolve dependência entre eventos nem heterogeneidade dentro de ano.
2. **Deslocamento circular anual dos CARs:** desloca conjuntamente a série de somas de cinco dias em cada ano por pelo menos 20 posições válidas, preservando boa parte da dependência e o calendário relativo dos eventos. Teste contra centro empírico da distribuição, que pode ser não zero. O corte circular cria emendas e supõe comparabilidade dentro de ano; não é teste exato.
3. **Placebos anuais para todos os eventos:** mantém número de eventos por ano e exclui a vizinhança de toda a lista original; amostragem com reposição. Não respeita toda dependência entre CARs. Não é o contraste domésticos–externos.

| lista | variavel | teste | n_dom | n_ext | estatistica | p | referencia_nula |
|---|---|---|---|---|---|---|---|
| completa | agio_anormal | Original rótulos irrestritos | 50 | 53 | 0.071580327 | 0.7656 | 0 |
| completa | agio_anormal | Rótulos dentro de ano; CAR centrado por ano | 50 | 53 | 0.03495879 | 0.87622476 | 0 |
| completa | agio_anormal | Deslocamento circular anual CAR, mínimo 20 posições | 50 | 53 | 0.071580327 | 0.94121176 | 0.086151331 |
| completa | agio_anormal | Placebos todos eventos estratificados por ano | nan | nan | -0.17516245 | 0.24995001 | -0.0663526 |
| completa | agio_ajustado_dolar | Original rótulos irrestritos | 50 | 53 | 0.11642408 | 0.6022 | 0 |
| completa | agio_ajustado_dolar | Rótulos dentro de ano; CAR centrado por ano | 50 | 53 | 0.088314624 | 0.67146571 | 0 |
| completa | agio_ajustado_dolar | Deslocamento circular anual CAR, mínimo 20 posições | 50 | 53 | 0.11642408 | 0.86682663 | 0.084584913 |
| completa | agio_ajustado_dolar | Placebos todos eventos estratificados por ano | nan | nan | -0.030601162 | 0.27814437 | 0.071653397 |
| sem_sobrepostos | agio_anormal | Original rótulos irrestritos | 32 | 15 | 0.75708347 | 0.0526 | 0 |
| sem_sobrepostos | agio_anormal | Rótulos dentro de ano; CAR centrado por ano | 32 | 15 | 0.53050563 | 0.14957009 | 0 |
| sem_sobrepostos | agio_anormal | Deslocamento circular anual CAR, mínimo 20 posições | 32 | 15 | 0.75708347 | 0.18036393 | 0.32065149 |
| sem_sobrepostos | agio_anormal | Placebos todos eventos estratificados por ano | nan | nan | -0.26549777 | 0.43911218 | -0.15206247 |
| sem_sobrepostos | agio_ajustado_dolar | Original rótulos irrestritos | 32 | 15 | 0.79738799 | 0.033 | 0 |
| sem_sobrepostos | agio_ajustado_dolar | Rótulos dentro de ano; CAR centrado por ano | 32 | 15 | 0.58538437 | 0.094181164 | 0 |
| sem_sobrepostos | agio_ajustado_dolar | Deslocamento circular anual CAR, mínimo 20 posições | 32 | 15 | 0.79738799 | 0.13577285 | 0.3091081 |
| sem_sobrepostos | agio_ajustado_dolar | Placebos todos eventos estratificados por ano | nan | nan | -0.093129291 | 0.5194961 | 0.002881379 |

Na lista completa, a ausência de evidência de diferença permanece. Na lista isolada ajustada, p original=0,033; rótulos anuais p=0,09418 e deslocamento circular p=0,13577. A evidência não se mantém a 5% nessas alternativas. Não significa que a diferença seja zero. No anormal isolado, p=0,0526 originalmente, versus 0,14957/0,18036 nos suplementos. IC dos contrastes não foi estimado: percentis da distribuição nula não foram rotulados como IC do efeito. EP Monte Carlo aproximado no original p=0,033 é 0,00253 (intervalo de precisão aproximado ±0,00495 a 95%).

Apenas recalcular os rótulos de sobreposição pelo calendário PTAX, em memória, deixa 60 eventos isolados (32 domésticos,14 externos e14 monetários): anormal diferença=0,83846/p=0,0434; ajustado=0,85480/p=0,0306. Esse diagnóstico revela a consequência do erro de calendário; não autoriza escolher o resultado mais significativo e não modifica eventos.csv.

## Repasse: identidade e estimandos diferentes

Se A=P/X−1, então log(P_t/P_{t−1})−log(X_t/X_{t−1})=log(1+A_t)−log(1+A_{t−1}). A identidade foi verificada com preço consolidado implícito P=X(1+A), erro máximo 3,84e−14 em 100×log. Esse preço agrega corretoras com pesos variáveis; não é necessariamente um preço transacionável único. Já ágio anormal=100A−mediana anterior de 100A. Portanto regressão em ágio anormal não equivale à regressão em retorno nem à variação diária do ágio.

| variavel | coeficiente | erro_padrao | t | p_valor | dependente |
|---|---|---|---|---|---|
| d_dolar | 0.85621357 | 0.017590745 | 48.674095 | 0 | ret_usdt |
| d_dolar | -0.1443142 | 0.017692303 | -8.1568916 | 3.4375662e-16 | delta_agio |
| d_dolar | -0.12899693 | 0.013453144 | -9.5886079 | 8.9281465e-22 | agio_anormal |

Com controles idênticos, coeficiente do retorno USDT é 0,85621 e da variação do ágio é −0,14431; o ágio anormal dá −0,12900. São associações, não elasticidades causais identificadas. Soma original dos lags 1–3=−0,07978, p=0,00025397; somar contemporâneo e lags não transforma a equação em resposta causal acumulada. V4b/V6 compartilham estatística, não identificam motivo de venda. Os valores-p originais são bilaterais mais verificação do sinal, não unilaterais.

## Hipóteses e multiplicidade

| hipotese | descricao | estimativa | p_valor | sinal_previsto | p_holm | confirma | confirma_holm |
|---|---|---|---|---|---|---|---|
| V1 | Estresse fiscal eleva o ágio | juro 0.0019; dom−ext 0.072 | 0.7656 | True | 1 | nao | nao |
| V2 | Crises elevam a participação | CAR negócios 0.426 | 0.631 | False | 1 | nao | nao |
| V3 | Medo global eleva o ágio | VIX anterior 0.0156 | 0.0078359438 | True | 0.031343775 | sim | sim |
| V4a | Repasse incompleto no dia | dólar -0.1290 | 8.9281465e-22 | True | 6.2497026e-21 | sim | sim |
| V4b | Repasse se completa depois | soma defasagens -0.0798 | 0.00025396701 | False | 0.0015238021 | nao | nao |
| V6 | Realização de ganhos: ágio segue caindo depois | soma defasagens -0.0798 | 0.00025396701 | True | 0.0015238021 | sim | sim |
| V5 | Choques externos isolados reduzem o ágio | CAR externos -0.614 (n=15) | 0.0348 | True | 0.1044 | sim | nao |

V1/V2 são originais do TCC conforme diário; V3/V4a/V5 derivam da descoberta; V4b foi formulada para validação e o adendo registra seu resultado contrário; V6 deriva desse resultado em 01/11/2026. V4b e V6 têm p e Holm idênticos, com sinais opostos: apenas uma pode confirmar pelo sinal. A dependência não invalida o algoritmo de Holm, mas o conjunto não oferece sete evidências independentes. V6 também tem confirma_holm=sim na descoberta, embora o resumo textual mencione só V3/V4a: nenhum desses “sim” é confirmação fora da amostra.

A escolha de eventos/modelos após observar a descoberta não é corrigida por Holm sobre apenas sete hipóteses. A inferência sequencial planejada também não foi calibrada: duas oportunidades de decisão com 1%/5% não garantem conjuntamente 5%; o limite de união é até 6%, não uma estimativa de erro efetivo. Recomendação é esclarecer via adendo futuro o orçamento de erro e a interpretação da intermediária. Nenhum pré-registro foi editado.
