# Pré-registro da validação fora da amostra

*Registrado em 01/11/2026, antes de qualquer dado posterior a 30/10/2026 ser coletado ou analisado. Este arquivo não deve ser editado depois do início da validação; mudanças entram como adendo datado no fim, com o motivo.*

## Por que validar fora da amostra

Todos os testes do TCC até aqui usaram os dados de out/2020 a out/2026 (**amostra de descoberta**). A hipótese fiscal foi fixada antes dos testes, mas os resultados que apareceram depois (medo global e repasse incompleto do câmbio) surgiram ao olhar esses mesmos dados. Para que eles possam ser afirmados, e não só sugeridos, precisam ser confirmados em dados que ainda não existiam quando as hipóteses foram escritas (**amostra de validação**).

## Amostras

| Amostra | Período | Uso |
| --- | --- | --- |
| Descoberta | 13/10/2020 a 30/10/2026 | Exploração e teste da hipótese original. Já analisada. |
| Validação intermediária | 02/11/2026 a 29/10/2027 (cerca de 250 dias úteis) | Checagem com critério mais rígido (1%). |
| Validação final | 02/11/2026 a 31/10/2028 (cerca de 500 dias úteis) | Decisão (5%). |

O ágio anormal usa a mediana dos 60 dias úteis anteriores, que pode incluir dias da amostra de descoberta; isso não usa nenhum resultado, só o nível do ágio.

Comando: `agio testar --inicio 2026-11-02 --fim 2027-10-30` (intermediária) e `agio testar --inicio 2026-11-02 --fim 2028-11-01` (final). Cada análise roda **uma vez** na data prevista.

## Coleta durante a validação

- `agio coletar`, `agio coletar-horario` e `agio coletar-controles` rodam pelo menos uma vez por semana (as APIs das corretoras não garantem histórico longo).
- Nenhuma mudança de código na medida do ágio, nos controles ou nos testes durante a validação, a não ser correção de erro, registrada em `decisoes.md` com o motivo e sem olhar resultados da validação.

## Eventos da validação

- **Agendados:** gerados pela mesma regra (`scripts/montar_eventos.py`): decisões do Copom e do Fed, PLDO, PLOA, relatórios bimestrais. Os calendários de 2027 e 2028 entram assim que publicados.
- **Não agendados:** mesmo critério da descoberta (anúncio de mudança nas regras fiscais ou medida extraordinária para cumprir a meta; choque externo com cobertura na imprensa econômica; norma do BC sobre criptoativos). Cada evento entra **até 30 dias depois de acontecer, com fonte, e sempre antes de qualquer análise da validação**.
- O primeiro turno de 2028 é eleição municipal e **não** entra (a regra é eleição presidencial).

## Hipóteses e regras de decisão

Todas as regressões: MQO com erros de Newey-West (5 defasagens), mesmos controles da descoberta. Estudo de evento: janela de −1 a +3 dias úteis, permutação com 5.000 sorteios, semente 42.

| # | Hipótese | Origem | Teste | Confirma se |
| --- | --- | --- | --- | --- |
| V1 | O estresse fiscal eleva o ágio | Hipótese original do TCC | Coeficiente de `d_juro_bp` na regressão do ágio anormal **e** CAR de domésticos maior que de externos (lista completa) | Coeficiente > 0 com p < α **e** diferença > 0 com p de permutação < α |
| V2 | Crises elevam a participação | Hipótese comportamental do TCC | CAR do número de negócios anormal, todos os eventos, contra datas sorteadas | CAR > média placebo com p de permutação < α |
| V3 | O medo global eleva o ágio | Descoberta (regressão e robustez) | Coeficiente de `d_vix_ant` | > 0 com p < α |
| V4a | Repasse incompleto do câmbio no dia | Descoberta (todas as especificações) | Coeficiente de `d_dolar` | < 0 com p < α |
| V4b | O repasse se completa nos dias seguintes | Nova (não testada na descoberta como confirmatória) | Soma dos coeficientes de `d_dolar` defasado 1 a 3 dias (`regressao_repasse`) | > 0 com p < α |
| V5 | Choques externos isolados reduzem o ágio | Descoberta (exploratória, estudo de evento) | CAR do ágio ajustado pelo dólar, externos sem sobreposição | < média placebo com p de permutação < α |

- **α = 1%** na validação intermediária e **α = 5%** na final. A conclusão do TCC usa a final; a intermediária só permite antecipar uma confirmação.
- **Testes múltiplos:** além do p de cada hipótese, o relatório mostra os p-valores ajustados pelo método de Holm para as seis hipóteses. A conclusão menciona os dois.
- **Sem poder:** se uma hipótese de evento tiver menos de 10 eventos na validação, o resultado é declarado inconclusivo, não negativo.
- **Resultado contrário** (por exemplo, coeficiente significativo com o sinal oposto) é registrado como tal.

## O que já se sabe da descoberta (para comparação)

| # | Descoberta |
| --- | --- |
| V1 | Juro: 0,0019 (p = 0,088). Domésticos − externos: +0,07 (p = 0,77). Não confirmada. |
| V2 | Negócios, todos os eventos: p de permutação = 0,63. Não confirmada. |
| V3 | 0,016 (p = 0,008); significativo em 7 de 9 especificações de robustez. |
| V4a | −0,129 (p < 0,001); significativo em todas as especificações alinhadas à PTAX. |
| V4b | Ainda não estimada. |
| V5 | −0,61 p.p. (p = 0,035), 15 eventos; um entre cerca de 40 testes. |

## Adendo 1 (01/11/2026, antes de qualquer dado da validação)

**Motivo.** A V4b foi escrita antes de estimar a regressão de repasse. Na amostra de descoberta ela saiu com o sinal contrário ao previsto: depois de uma alta do dólar oficial, o ágio continua caindo nos dois dias seguintes (defasagens de 1 e 2 dias: −0,057 e −0,025; soma das 3 defasagens: −0,080, p < 0,001). O efeito total chega a cerca de −0,21 p.p. por 1% de alta, contra −0,13 só no dia.

**O que muda.**
- A **V4b fica como foi escrita** e será testada na validação com o sinal original (soma > 0). Na descoberta, ela não se confirma.
- Entra a **V6, derivada da descoberta:** "realização de ganhos". Quem tem USDT vende ao longo de alguns dias depois de uma alta do dólar, e o ágio continua caindo.
  - Teste: a mesma soma das defasagens 1 a 3 de `regressao_repasse`.
  - Confirma se a soma for < 0 com p < α.
  - A V6 surgiu nos dados da descoberta; a confirmação depende só da validação.
- A correção de Holm passa a cobrir 7 hipóteses (V1, V2, V3, V4a, V4b, V5 e V6), e o quadro mostra a decisão pelo p simples (`confirma`) e pelo p ajustado (`confirma_holm`).

**Situação na descoberta, pelo p ajustado de Holm.** V3 (0,031) e V4a (< 0,001) se mantêm. A V5 cai (0,104), e por isso deve ser lida como fraca.
