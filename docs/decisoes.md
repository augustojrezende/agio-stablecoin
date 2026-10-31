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
