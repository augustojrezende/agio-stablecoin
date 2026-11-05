# AUD-001 — Relatório executivo

**Parecer: os números centrais da descoberta são reproduzíveis, mas o TCC requer ajustes antes de ser apresentado como metodologicamente pronto.** A ausência de confirmação fiscal deve ser preservada como resultado válido; não autoriza concluir irrelevância fiscal. Os dados não identificam realização de ganhos, falta de vendedores ou causa local específica do episódio de 2026.

Auditoria de 02/11/2026, branch main, commit `543fdea26bc734fbea6d0fa712e5213c0d75d06a`. Objetivo: verificar integridade, reconstrução, inferência e coerência, preservando integralmente o histórico de descoberta de 13/10/2020 a 30/10/2026. Escopo: todos os módulos de coleta/transformação/análise/relatório, 46 CSVs oficiais, 158 eventos, dez figuras solicitadas e uma adicional, pré-registro/diário/narrativa e 41 testes existentes. Dados brutos foram reutilizados; não houve novas consultas de séries históricas.

## Contagens e síntese

**36 verificações registradas na matriz**, além dos 41 testes automatizados existentes (todos aprovados). As contagens abaixo incluem verificações aprovadas e inconclusivas; não são 36 erros.

| gravidade | quantidade |
|---|---|
| crítica | 0 |
| alta | 14 |
| média | 9 |
| baixa | 3 |
| informativa | 10 |

| classificação | quantidade |
|---|---|
| Verificação concluída sem problemas | 10 |
| Erro comprovado | 7 |
| Inconsistência documental | 4 |
| Risco metodológico | 9 |
| Limitação conhecida e adequadamente documentada | 3 |
| Verificação inconclusiva por falta de evidência | 2 |
| Oportunidade de melhoria | 1 |

Não foi demonstrado achado crítico que invalide toda a amostra. Há **7 erros comprovados** de implementação/apresentação, com alcance delimitado abaixo. Riscos potenciais não foram promovidos a erros confirmados.

## Principais achados

1. CLI robustez falha com os lotes atuais por índices pandas duplicados. Nove especificações recalculadas em memória coincidem com as oficiais: falha de execução não é evidência de coeficientes incorretos.
2. Copom 28/10/2021 e Fed 04/11/2021 estão incorretamente marcados como não sobrepostos no calendário efetivo.
3. Mediana da Figura 01 inclui o próprio dia, apesar de ser descrita como normal usado no anormal; a análise estatística exclui corretamente esse dia.
4. Rótulos de n nas trajetórias contam eventos cujos valores são NaN; n efetivo é menor e por vezes varia ao longo da curva.
5. Volume do episódio está descrito em reais, mas representa USDT.
6. V1 não aplica a regra registrada de insuficiência de eventos; exemplo com dois eventos retorna nao em vez de inconclusivo. Afeta validação futura, não a contagem atual.
7. Família de Holm cai de sete para seis hipóteses quando V5 não é estimável; o quadro atual com sete está correto.

## Resultados que podem ser mantidos

Amostra: 1520 dias, 1490 na regressão principal. Dólar −0,128997 (p≈8,93e−22); juro +0,001927 (p=0,08756); VIX +0,021235 (p=0,04682); VIX anterior +0,015634 (p=0,007836). R²=0,09535 e curtose residual=15,3378. HAC independente e mediana independente confirmaram cálculos. Holm das sete hipóteses atuais é correto.

As quatro exclusões estão reconciliadas: Copom 29/10/2020, Fed 06/11/2020 e fiscal 21/11/2020 por falta de histórico/janela; Fed 29/10/2026 por janela posterior incompleta. Domésticos são apenas fiscal/político, conforme desenho. Os 154 eventos não indicam perda silenciosa inexplicada.

Os 14 tratados, 30 resultados diretamente regenerados e nove especificações recalculadas coincidem no recorte; a base_teste reproduz todas as colunas antigas e acrescenta quatro colunas Trends. Dez figuras solicitadas e a figura do episódio foram reproduzidas byte a byte (episódio em processo separado). Isso confirma rastreabilidade dos gráficos, não sua validade interpretativa.

## Sensibilidades e riscos científicos

- Comparação isolada ajustada: diferença +0,7974, p original=0,033. Permutação dentro de ano: estatística centrada +0,5854, p=0,09418; deslocamento circular anual: diferença bruta +0,7974, p=0,13577. Evidência é sensível à referência temporal, sem prova de efeito nulo.
- HAC10/20 preserva sinais principais, mas retirada dos cinco casos de maior Cook leva VIX anterior a p=0,09984. Não selecionar esse suplemento nem a versão original por significância; reportar a sensibilidade.
- VIX contemporâneo é informação posterior à janela PTAX. A limitação já era reconhecida. Resultados são associações ex post, sem identificação causal.
- A família Holm atual está correta, mas não desfaz exploração anterior nem resolve decisões intermediária/final com 1%/5%. V4b/V6 são sentidos opostos da mesma estatística.
- Ágio anormal é nível relativo à mediana; repasse exige separar identidade matemática de retorno, associação observada e mecanismo. Não inferir vendas para realização de ganhos.
- Junho/julho apresenta prêmio persistente em ambas as fontes; o teste de oferta global não autoriza descartar escassez. Médias publicadas abrangem junho–meados de agosto, não apenas o núcleo de alta.

## Recomendações prioritárias

**P1:** resolver futuramente falha de robustez e calendário de sobreposições; corrigir regras de elegibilidade/família para validação; publicar errata metodológica para causalidade, mecanismo, não significância e regra sequencial; verificar fontes/horários fiscais pendentes. Qualquer mudança depende do pesquisador e deve preservar o original.

**P2:** alinhar legenda/mediana, n efetivo, unidades do episódio e conceitos de faixas; apresentar sensibilidades e métricas de cobertura; identificar vintages e proveniência. **P3:** registrar bundle de dados/versões e atualizar estado documental do Trends. Nenhuma correção foi aplicada.

## Limitações e situação dos critérios de aceite

| critério | requisito | situação |
|---|---|---|
| 1 | Baseline preservada | Atendido; SHA-256 antes/depois |
| 2 | Commit identificado | Atendido |
| 3 | Hashes comparados | Atendido; integridade_final.json |
| 4 | Pipeline reproduzido ou limites documentados | Atendido com ressalva: CLI robustez falha; números recalculados |
| 5 | Quatro exclusões explicadas | Atendido |
| 6 | Permutações examinadas | Atendido; suplementos e limites registrados |
| 7 | Domésticos versus externos auditado | Atendido |
| 8 | Repasse avaliado | Atendido; mecanismo não identificado |
| 9 | Hipóteses/Holm verificados | Atendido; falhas de fronteira e regra sequencial registradas |
| 10 | Figuras/tabelas confrontadas | Atendido; dez figuras + episódio |
| 11 | Achados classificados | Atendido |
| 12 | Ajustes separados da baseline | Atendido |
| 13 | Implementação não modificada | Atendido |
| 14 | Sem commits/pushes | Atendido |

A entrega da auditoria cobre os critérios, mas **não constitui aprovação metodológica integral nem reprodução integral sem ressalvas do comando de pipeline**. Permanecem inconclusivas a autenticidade externa de cada dado/horário, todas as datas fiscais efetivas e a prioridade histórica independente das hipóteses. Não se produziu validação fora da amostra. A lista completa de limitações está na matriz/reprodutibilidade.

## Parecer final

**Pronto para discutir resultados de descoberta com ressalvas explícitas; ainda não pronto para conclusão causal ou confirmação definitiva das hipóteses.** Após resolver erros demonstrados e ambiguidades de protocolo/documentação, reavaliar prontidão sem exigir significância fiscal ou global. Os resultados não significativos podem e devem permanecer. Causa do episódio e motivação comportamental devem permanecer questões abertas.

## Entregáveis

- AUD-001_RELATORIO_EXECUTIVO.md
- AUD-001_MATRIZ_ACHADOS.md
- AUD-001_REPRODUTIBILIDADE.md
- AUD-001_SENSIBILIDADE.md
- AUD-001_PLANO_AJUSTES.md

Anexos CSV/JSON/logs/scripts preservam evidência e parâmetros. Hashes finais confirmam preservação dos 154 arquivos protegidos; somente esta pasta de auditoria foi criada, sem commits/pushes.
