# AUD-002 — Comparativo V1/V2

Versão V2 / AUD-002. Origem: `543fdea26bc734fbea6d0fa712e5213c0d75d06a`. Data de fechamento: 02/11/2026.

## Leitura das diferenças

O pipeline usa corte histórico 30/10/2026, semente 42, 5.000 permutações, janela de eventos −1 a +3, MQO/Newey-West e HAC de cinco defasagens. Não houve alteração desses parâmetros. O replay dos brutos reproduz os 14 tratados de referência; dados brutos posteriores ao corte não entram na análise.

Os 46 CSVs oficiais são comparados abaixo (tolerância absoluta 1e-10 e relativa 1e-8). `alteracoes` conta células alteradas ou linhas ausentes conforme o comparador; colunas novas são listadas separadamente. O registro célula a célula com valores anteriores/novos está em `diferencas_celulas.csv` e integra este comparativo.

As únicas exclusões são os dois eventos antes falsamente isolados. Por isso mudam os três estudos de grupos isolados e seus contrastes. Valores-p de permutação podem mudar também com o conjunto elegível e a sequência de consumo do mesmo gerador aleatório, sem troca de semente. As quatro colunas de buscas em base_teste são enriquecimento da etapa relatorio do pipeline completo; não alteram as colunas comuns nem as regressões. `n_domesticos/n_externos` tornam explícita a elegibilidade V1; `estimavel` explicita disponibilidade. Nenhuma dessas adições representa nova hipótese.

Contraste isolado de ágio anormal: diferença 0,75708347 → 0,83846047, p 0,0526 → 0,0434. Contraste ajustado pelo dólar: 0,79738799 → 0,85479530, p 0,0330 → 0,0306. Todos os demais valores alterados, inclusive negócios e grupos, estão no anexo célula a célula abaixo. O conjunto completo de eventos mantém 154 válidos e suas estimativas.

V5: CAR externo isolado −0,614 (n=15) → −0,671 (n=14); p bruto 0,0348 → 0,024; Holm 0,1044 → 0,072. As decisões finais permanecem: V1/V2/V4b não confirmadas; V3/V4a/V6 compatíveis com o sinal previsto e significativas após Holm nesta amostra; V5 apenas no teste bruto. Isso não constitui validação fora da amostra nem confirmação causal.

## CSVs

| arquivo_v1 | arquivo_v2 | n_v1 | n_v2 | colunas_novas | alteracoes | max_dif_absoluta_comuns |
| --- | --- | --- | --- | --- | --- | --- |
| dados/tratado/agio_diario.csv | dados/tratado_v2/agio_diario.csv | 1520 | 1520 |  | 0 | 0.0 |
| dados/tratado/agio_fechamento_diario.csv | dados/tratado_v2/agio_fechamento_diario.csv | 1520 | 1520 |  | 0 | 0.0 |
| dados/tratado/agio_fechamento_por_fonte.csv | dados/tratado_v2/agio_fechamento_por_fonte.csv | 2434 | 2434 |  | 0 | 0.0 |
| dados/tratado/agio_por_fonte.csv | dados/tratado_v2/agio_por_fonte.csv | 2434 | 2434 |  | 0 | 0.0 |
| dados/tratado/google_trends.csv | dados/tratado_v2/google_trends.csv | 4502 | 4502 |  | 0 | 0.0 |
| dados/tratado/juro_real_10a.csv | dados/tratado_v2/juro_real_10a.csv | 5314 | 5314 |  | 0 | 0.0 |
| dados/tratado/painel_diario.csv | dados/tratado_v2/painel_diario.csv | 1520 | 1520 |  | 0 | 0.0 |
| dados/tratado/precos_janela_ptax.csv | dados/tratado_v2/precos_janela_ptax.csv | 3537 | 3537 |  | 0 | 0.0 |
| dados/tratado/precos_usdt_brl.csv | dados/tratado_v2/precos_usdt_brl.csv | 3539 | 3539 |  | 0 | 0.0 |
| dados/tratado/ptax.csv | dados/tratado_v2/ptax.csv | 1527 | 1527 |  | 0 | 0.0 |
| dados/tratado/selic.csv | dados/tratado_v2/selic.csv | 1527 | 1527 |  | 0 | 0.0 |
| dados/tratado/sinais_comportamento.csv | dados/tratado_v2/sinais_comportamento.csv | 3539 | 3539 |  | 0 | 0.0 |
| dados/tratado/usdt_oferta.csv | dados/tratado_v2/usdt_oferta.csv | 3258 | 3258 |  | 0 | 0.0 |
| dados/tratado/vix.csv | dados/tratado_v2/vix.csv | 9306 | 9306 |  | 0 | 0.0 |
| dados/resultados/base_buscas.csv | dados/resultados_v2/base_buscas.csv | 1520 | 1520 |  | 0 | 0.0 |
| dados/resultados/base_teste.csv | dados/resultados_v2/base_teste.csv | 1520 | 1520 | busca_dolar_anormal,busca_dólar,busca_usdt,busca_usdt_anormal | 0 | 0.0 |
| dados/resultados/episodio_20260601_20260815.csv | dados/resultados_v2/episodio_20260601_20260815.csv | 115 | 115 |  | 0 | 0.0 |
| dados/resultados/eventos_agio_ajustado_dolar.csv | dados/resultados_v2/eventos_agio_ajustado_dolar.csv | 154 | 154 |  | 0 | 0.0 |
| dados/resultados/eventos_agio_ajustado_dolar_sem_sobrepostos.csv | dados/resultados_v2/eventos_agio_ajustado_dolar_sem_sobrepostos.csv | 62 | 60 |  | 2 | 0.0 |
| dados/resultados/eventos_agio_anormal.csv | dados/resultados_v2/eventos_agio_anormal.csv | 154 | 154 |  | 0 | 0.0 |
| dados/resultados/eventos_agio_anormal_sem_sobrepostos.csv | dados/resultados_v2/eventos_agio_anormal_sem_sobrepostos.csv | 62 | 60 |  | 2 | 0.0 |
| dados/resultados/eventos_comparacao_agio_ajustado_dolar.csv | dados/resultados_v2/eventos_comparacao_agio_ajustado_dolar.csv | 1 | 1 | n_domesticos,n_externos | 0 | 0.0 |
| dados/resultados/eventos_comparacao_agio_ajustado_dolar_sem_sobrepostos.csv | dados/resultados_v2/eventos_comparacao_agio_ajustado_dolar_sem_sobrepostos.csv | 1 | 1 | n_domesticos,n_externos | 3 | 0.05740730704217589 |
| dados/resultados/eventos_comparacao_agio_anormal.csv | dados/resultados_v2/eventos_comparacao_agio_anormal.csv | 1 | 1 | n_domesticos,n_externos | 0 | 0.0 |
| dados/resultados/eventos_comparacao_agio_anormal_sem_sobrepostos.csv | dados/resultados_v2/eventos_comparacao_agio_anormal_sem_sobrepostos.csv | 1 | 1 | n_domesticos,n_externos | 3 | 0.08137699894157946 |
| dados/resultados/eventos_comparacao_negocios_anormal.csv | dados/resultados_v2/eventos_comparacao_negocios_anormal.csv | 1 | 1 | n_domesticos,n_externos | 0 | 0.0 |
| dados/resultados/eventos_comparacao_negocios_anormal_sem_sobrepostos.csv | dados/resultados_v2/eventos_comparacao_negocios_anormal_sem_sobrepostos.csv | 1 | 1 | n_domesticos,n_externos | 3 | 0.11760000000000004 |
| dados/resultados/eventos_grupos_agio_ajustado_dolar.csv | dados/resultados_v2/eventos_grupos_agio_ajustado_dolar.csv | 8 | 8 |  | 0 | 0.0 |
| dados/resultados/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | 7 | 7 |  | 23 | 2.0 |
| dados/resultados/eventos_grupos_agio_anormal.csv | dados/resultados_v2/eventos_grupos_agio_anormal.csv | 8 | 8 |  | 0 | 0.0 |
| dados/resultados/eventos_grupos_agio_anormal_sem_sobrepostos.csv | dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | 7 | 7 |  | 23 | 2.0 |
| dados/resultados/eventos_grupos_negocios_anormal.csv | dados/resultados_v2/eventos_grupos_negocios_anormal.csv | 8 | 8 |  | 0 | 0.0 |
| dados/resultados/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | 7 | 7 |  | 23 | 2.0 |
| dados/resultados/eventos_negocios_anormal.csv | dados/resultados_v2/eventos_negocios_anormal.csv | 154 | 154 |  | 0 | 0.0 |
| dados/resultados/eventos_negocios_anormal_sem_sobrepostos.csv | dados/resultados_v2/eventos_negocios_anormal_sem_sobrepostos.csv | 62 | 60 |  | 2 | 0.0 |
| dados/resultados/exploratorio_atencao.csv | dados/resultados_v2/exploratorio_atencao.csv | 8 | 8 |  | 0 | 0.0 |
| dados/resultados/exploratorio_eventos_busca_dolar_anormal.csv | dados/resultados_v2/exploratorio_eventos_busca_dolar_anormal.csv | 8 | 8 |  | 0 | 0.0 |
| dados/resultados/exploratorio_eventos_busca_usdt_anormal.csv | dados/resultados_v2/exploratorio_eventos_busca_usdt_anormal.csv | 8 | 8 |  | 0 | 0.0 |
| dados/resultados/exploratorio_oferta_usdt.csv | dados/resultados_v2/exploratorio_oferta_usdt.csv | 7 | 7 |  | 0 | 0.0 |
| dados/resultados/hipoteses.csv | dados/resultados_v2/hipoteses.csv | 7 | 7 | estimavel | 3 | 0.032399999999999984 |
| dados/resultados/regressao_agio_anormal.csv | dados/resultados_v2/regressao_agio_anormal.csv | 6 | 6 |  | 0 | 0.0 |
| dados/resultados/regressao_negocios_anormal.csv | dados/resultados_v2/regressao_negocios_anormal.csv | 6 | 6 |  | 0 | 0.0 |
| dados/resultados/regressao_repasse.csv | dados/resultados_v2/regressao_repasse.csv | 9 | 9 |  | 0 | 0.0 |
| dados/resultados/regressao_repasse_soma.csv | dados/resultados_v2/regressao_repasse_soma.csv | 1 | 1 |  | 0 | 0.0 |
| dados/resultados/regressao_ticket_anormal.csv | dados/resultados_v2/regressao_ticket_anormal.csv | 6 | 6 |  | 0 | 0.0 |
| dados/resultados/robustez.csv | dados/resultados_v2/robustez.csv | 9 | 9 |  | 0 | 0.0 |

## Todas as células/linhas divergentes

| arquivo | chave | coluna | v1 | v2 |
| --- | --- | --- | --- | --- |
| dados/resultados_v2/eventos_agio_ajustado_dolar_sem_sobrepostos.csv | data=2021-10-28; tipo=monetario; descricao=Decisão do Copom | linha | presente | ausente |
| dados/resultados_v2/eventos_agio_ajustado_dolar_sem_sobrepostos.csv | data=2021-11-04; tipo=externo; descricao=Decisão do Fed (FOMC) | linha | presente | ausente |
| dados/resultados_v2/eventos_agio_anormal_sem_sobrepostos.csv | data=2021-10-28; tipo=monetario; descricao=Decisão do Copom | linha | presente | ausente |
| dados/resultados_v2/eventos_agio_anormal_sem_sobrepostos.csv | data=2021-11-04; tipo=externo; descricao=Decisão do Fed (FOMC) | linha | presente | ausente |
| dados/resultados_v2/eventos_comparacao_agio_ajustado_dolar_sem_sobrepostos.csv | __row__=0 | car_externos | -0.6136568062993241 | -0.6710641133415 |
| dados/resultados_v2/eventos_comparacao_agio_ajustado_dolar_sem_sobrepostos.csv | __row__=0 | diferenca | 0.7973879886609845 | 0.8547952957031604 |
| dados/resultados_v2/eventos_comparacao_agio_ajustado_dolar_sem_sobrepostos.csv | __row__=0 | p_valor_permutacao | 0.033 | 0.0306 |
| dados/resultados_v2/eventos_comparacao_agio_anormal_sem_sobrepostos.csv | __row__=0 | car_externos | -0.7565932994921769 | -0.8379702984337564 |
| dados/resultados_v2/eventos_comparacao_agio_anormal_sem_sobrepostos.csv | __row__=0 | diferenca | 0.7570834681283939 | 0.8384604670699733 |
| dados/resultados_v2/eventos_comparacao_agio_anormal_sem_sobrepostos.csv | __row__=0 | p_valor_permutacao | 0.0526 | 0.0434 |
| dados/resultados_v2/eventos_comparacao_negocios_anormal_sem_sobrepostos.csv | __row__=0 | car_externos | 0.9734516301637712 | 0.8693941800686252 |
| dados/resultados_v2/eventos_comparacao_negocios_anormal_sem_sobrepostos.csv | __row__=0 | diferenca | -0.4594106381165326 | -0.3553531880213866 |
| dados/resultados_v2/eventos_comparacao_negocios_anormal_sem_sobrepostos.csv | __row__=0 | p_valor_permutacao | 0.4516 | 0.5692 |
| dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | tipo=agendado=nao | p_valor_permutacao | 0.2094 | 0.207 |
| dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | tipo=agendado=sim | n | 55 | 53 |
| dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | tipo=agendado=sim | car_medio | -0.043464197574771 | -0.07638790380294944 |
| dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | tipo=agendado=sim | t | -0.27760236225645224 | -0.4779089404505734 |
| dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | tipo=agendado=sim | p_valor_t | 0.7823776718171875 | 0.6347179931695761 |
| dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | tipo=agendado=sim | p_valor_permutacao | 0.6552 | 0.4744 |
| dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | tipo=externo | n | 15 | 14 |
| dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | tipo=externo | car_medio | -0.6136568062993241 | -0.6710641133415 |
| dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | tipo=externo | t | -1.6458463790751672 | -1.69575667404666 |
| dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | tipo=externo | p_valor_t | 0.12205147219649107 | 0.11373316141638015 |
| dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | tipo=externo | p_valor_permutacao | 0.0348 | 0.024 |
| dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | tipo=fiscal | p_valor_permutacao | 0.347 | 0.372 |
| dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | tipo=monetario | n | 15 | 14 |
| dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | tipo=monetario | car_medio | -0.16323745071473011 | -0.27975316452669474 |
| dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | tipo=monetario | t | -0.6701087346930036 | -1.217412254130178 |
| dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | tipo=monetario | p_valor_t | 0.5136906670039495 | 0.2450852000922765 |
| dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | tipo=monetario | p_valor_permutacao | 0.5016 | 0.2768 |
| dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | tipo=politico | p_valor_permutacao | 0.484 | 0.4804 |
| dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | tipo=todos | n | 62 | 60 |
| dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | tipo=todos | car_medio | -0.09312929063931734 | -0.12386740090969318 |
| dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | tipo=todos | t | -0.6362277057781321 | -0.8320194737644517 |
| dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | tipo=todos | p_valor_t | 0.5270081397233382 | 0.4087529749940099 |
| dados/resultados_v2/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | tipo=todos | p_valor_permutacao | 0.4074 | 0.2836 |
| dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | tipo=agendado=nao | p_valor_permutacao | 0.116 | 0.1174 |
| dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | tipo=agendado=sim | n | 55 | 53 |
| dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | tipo=agendado=sim | car_medio | -0.19879449392643336 | -0.23525789566219402 |
| dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | tipo=agendado=sim | t | -1.2438117817254413 | -1.4392826367519678 |
| dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | tipo=agendado=sim | p_valor_t | 0.21894132399164254 | 0.156063290504167 |
| dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | tipo=agendado=sim | p_valor_permutacao | 0.593 | 0.4 |
| dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | tipo=externo | n | 15 | 14 |
| dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | tipo=externo | car_medio | -0.7565932994921769 | -0.8379702984337564 |
| dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | tipo=externo | t | -1.9670143838172125 | -2.0751215740783793 |
| dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | tipo=externo | p_valor_t | 0.06932336414166089 | 0.058386364042645605 |
| dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | tipo=externo | p_valor_permutacao | 0.0364 | 0.022 |
| dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | tipo=fiscal | p_valor_permutacao | 0.5618 | 0.606 |
| dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | tipo=monetario | n | 15 | 14 |
| dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | tipo=monetario | car_medio | -0.3418431608678365 | -0.44856671653357577 |
| dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | tipo=monetario | t | -1.4055523110990358 | -1.9108097657891971 |
| dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | tipo=monetario | p_valor_t | 0.1816596817495438 | 0.07833244266860623 |
| dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | tipo=monetario | p_valor_permutacao | 0.4202 | 0.2374 |
| dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | tipo=politico | p_valor_permutacao | 0.9322 | 0.943 |
| dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | tipo=todos | n | 62 | 60 |
| dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | tipo=todos | car_medio | -0.265497766274859 | -0.29993054688639526 |
| dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | tipo=todos | t | -1.7521307807572848 | -1.9431845370979772 |
| dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | tipo=todos | p_valor_t | 0.08477678952845547 | 0.05676960944216553 |
| dados/resultados_v2/eventos_grupos_agio_anormal_sem_sobrepostos.csv | tipo=todos | p_valor_permutacao | 0.2988 | 0.1974 |
| dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | tipo=agendado=nao | p_valor_permutacao | 0.4398 | 0.4516 |
| dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | tipo=agendado=sim | n | 55 | 53 |
| dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | tipo=agendado=sim | car_medio | 0.626015603037417 | 0.5438112976257146 |
| dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | tipo=agendado=sim | t | 2.2894948716733907 | 1.9611135398107022 |
| dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | tipo=agendado=sim | p_valor_t | 0.02598555181440271 | 0.05523111805428245 |
| dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | tipo=agendado=sim | p_valor_permutacao | 0.4532 | 0.737 |
| dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | tipo=externo | n | 15 | 14 |
| dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | tipo=externo | car_medio | 0.9734516301637712 | 0.8693941800686252 |
| dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | tipo=externo | t | 1.4303397640753164 | 1.2033839745816386 |
| dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | tipo=externo | p_valor_t | 0.1745582780908368 | 0.250284729137898 |
| dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | tipo=externo | p_valor_permutacao | 0.2658 | 0.416 |
| dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | tipo=fiscal | p_valor_permutacao | 0.8702 | 0.9094 |
| dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | tipo=monetario | n | 15 | 14 |
| dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | tipo=monetario | car_medio | 0.6795578458649185 | 0.5010545876124668 |
| dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | tipo=monetario | t | 1.1267856488445565 | 0.8097187359929204 |
| dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | tipo=monetario | p_valor_t | 0.2787766505909603 | 0.4326737121973414 |
| dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | tipo=monetario | p_valor_permutacao | 0.627 | 0.9334 |
| dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | tipo=politico | p_valor_permutacao | 0.7196 | 0.731 |
| dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | tipo=todos | n | 62 | 60 |
| dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | tipo=todos | car_medio | 0.6652331271926125 | 0.5939265748841155 |
| dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | tipo=todos | t | 2.6539894995754936 | 2.3409123009579944 |
| dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | tipo=todos | p_valor_t | 0.010129936129624043 | 0.022635884716220595 |
| dados/resultados_v2/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | tipo=todos | p_valor_permutacao | 0.3528 | 0.5668 |
| dados/resultados_v2/eventos_negocios_anormal_sem_sobrepostos.csv | data=2021-10-28; tipo=monetario; descricao=Decisão do Copom | linha | presente | ausente |
| dados/resultados_v2/eventos_negocios_anormal_sem_sobrepostos.csv | data=2021-11-04; tipo=externo; descricao=Decisão do Fed (FOMC) | linha | presente | ausente |
| dados/resultados_v2/hipoteses.csv | descricao=Choques externos isolados reduzem o ágio; hipotese=V5 | estimativa | CAR externos -0.614 (n=15) | CAR externos -0.671 (n=14) |
| dados/resultados_v2/hipoteses.csv | descricao=Choques externos isolados reduzem o ágio; hipotese=V5 | p_valor | 0.0348 | 0.024 |
| dados/resultados_v2/hipoteses.csv | descricao=Choques externos isolados reduzem o ágio; hipotese=V5 | p_holm | 0.10439999999999999 | 0.07200000000000001 |

## Figuras

| figura | sha_v1 | sha_v2 | igual |
| --- | --- | --- | --- |
| 01_serie_agio.png | 49cfd11466975a38307b2e2c894458950de70d88fea6e7ff329765a7fde94430 | 54e50d07957623f0942ce0437702a8cb4ee85f7990dd32a255fe9c69dcec2fef | False |
| 02_janela_vs_fechamento.png | 65e07adce75a228f5c3efbc9fa192053272e812d0f5697e5cacc604944e2f613 | 65e07adce75a228f5c3efbc9fa192053272e812d0f5697e5cacc604944e2f613 | True |
| 03_agio_por_corretora.png | 02e1714cc900e6d1212b88cabf52645f2e5639ea1a720ce5cda61b68127aad8f | 02e1714cc900e6d1212b88cabf52645f2e5639ea1a720ce5cda61b68127aad8f | True |
| 04_agio_anormal_eventos.png | 380dc4bbf8baafa96ecd182446a9b3fdb3af3d1d211f6195f07f4d073596a93d | 380dc4bbf8baafa96ecd182446a9b3fdb3af3d1d211f6195f07f4d073596a93d | True |
| 05_dolar_e_agio.png | 356dfb875ccf031ca19bec4cc33c8540cf2119604628de8ebc8f19cc5d64274b | 356dfb875ccf031ca19bec4cc33c8540cf2119604628de8ebc8f19cc5d64274b | True |
| 06_trajetoria_agio.png | 67132ddc92bd3304bc56e186183c9c317dae6a2d0ccb3a3181119db1919455be | e84a2fba1400c3cb4f998fa555825f02cf621ec7da136843d9c347826b27368e | False |
| 07_trajetoria_negocios.png | c90a5194f8b58721c70f432a6501e93a6f5cd735cd9ba7e8a7e0802cfab97590 | c14d7e733b031727b42f0380e7b3e30329dced0f84ea97d6b1981c4d8e41fa86 | False |
| 08_robustez.png | 8cf1f8e3eb9b1cef8456945e1d349b29792aadd7b498e95dcbfd036667419748 | 8cf1f8e3eb9b1cef8456945e1d349b29792aadd7b498e95dcbfd036667419748 | True |
| 09_buscas_dolar.png | 599cc2cb38b72dd59c4917539c801ab1f6113a11a18310afce97fb178ada339b | fa2157c9df2e160a6c36815ebb7d56567a375ef6043e01c7dabc66810e71bfa5 | False |
| 09_buscas_usdt.png | ebf7b06cc4d55353bb71c15f49845abaec9117ca47352b01ed344804d8b811c3 | bbacb9269ae09a7be8842c9f889f94b5e4acdff7384fc91a1183ee4699a403b3 | False |
| episodio_20260601_20260815.png | e92a7d4790236a03c1e13bea105460fb20f5781ab0711c162c9cac44f4ebd004 | e92a7d4790236a03c1e13bea105460fb20f5781ab0711c162c9cac44f4ebd004 | True |

Figura 01 usa a mediana deslocada; figuras 06, 07 e 09 apresentam n válido por dia. As demais seis são idênticas.

## Trajetórias

| figura | tipo | n_v1 | n_v2_min | n_v2_max | medias_faixas_identicas |
| --- | --- | --- | --- | --- | --- |
| 06_trajetoria_agio | fiscal | 47 | 46 | 47 | True |
| 06_trajetoria_agio | externo | 54 | 53 | 53 | True |
| 06_trajetoria_agio | monetario | 48 | 47 | 47 | True |
| 07_trajetoria_negocios | fiscal | 47 | 46 | 47 | True |
| 07_trajetoria_negocios | externo | 54 | 53 | 53 | True |
| 07_trajetoria_negocios | monetario | 48 | 47 | 47 | True |
| 09_buscas_dolar | fiscal | 47 | 46 | 47 | True |
| 09_buscas_dolar | externo | 54 | 53 | 53 | True |
| 09_buscas_dolar | monetario | 48 | 47 | 47 | True |
| 09_buscas_usdt | fiscal | 47 | 46 | 47 | True |
| 09_buscas_usdt | externo | 54 | 53 | 53 | True |
| 09_buscas_usdt | monetario | 48 | 47 | 47 | True |

Médias/faixas placebo preservadas em todas as trajetórias; n nominal continua sendo o tamanho sorteado no placebo, sem mudança metodológica.

## Episódio

115 linhas preservadas. Médias de volume-base: 17.145.743,5885 → 26.068.573,2944 USDT (+52,0411%). Não foi publicado valor aproximado de conversão como volume financeiro exato. O texto histórico de docs/resultados.md recebeu apenas correção de unidade e aviso de escopo; as tabelas atuais estão em docs/v2.
