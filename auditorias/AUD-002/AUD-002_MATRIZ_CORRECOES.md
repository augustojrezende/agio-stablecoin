# AUD-002 — Matriz de correções

Versão V2 / AUD-002. Origem: `543fdea26bc734fbea6d0fa712e5213c0d75d06a`. Data de fechamento: 02/11/2026.

Fonte probatória: cinco documentos AUD-001 preservados em `../AUD-001/`, identificadores abaixo. Patch completo em `alteracoes_v2.patch`; novos testes em `tests/` na raiz do projeto.

| AUD-001 | Erro comprovado | Arquivos V2 | Correção | Testes e evidências | Impacto | Status |
|---|---|---|---|---|---|---|
| 06 | Índices duplicados impediam robustez | src/agio/cli.py | Concatenação com índice novo, deduplicação por chave e ordenação temporal | test_aud002.py; robustez_antes.log; robustez_v2_cli.log | 9 especificações iguais à baseline; candles preservados | Corrigido; testes aprovados |
| 10 | Sobreposição incorreta de Copom/Fed | scripts/montar_eventos.py; dados/manual/eventos_v2.csv | Interseção de janelas no calendário observado | test_aud002.py; diferencas_eventos.csv | 62 → 60 isolados; valores-p derivados alterados | Corrigido; testes aprovados |
| 21 | V1 sem controle de suficiência | src/agio/analise.py; docs/AUD-002_DECISOES_V2.md | Mínimo aprovado de 10 por grupo, ausente inconclusivo | test_aud002_hipoteses.py; hipoteses_antes.log; hipoteses_depois.log | Casos 0,2,9,10,11 e grupos ausentes cobertos; decisão atual igual | Corrigido; testes aprovados |
| 22 | V5 indisponível reduzia família Holm | src/agio/analise.py; docs/AUD-002_DECISOES_V2.md | Sete posições; p observado ausente; 1 interno conservador autorizado | test_aud002_hipoteses.py | Família completa preservada; cenários ausentes inconclusivos | Corrigido; testes aprovados |
| 26 | Mediana visual incluía o próprio dia | src/agio/relatorio.py | shift(1) e constantes do indicador | test_aud002.py | Figura 01 corrigida; indicador intacto | Corrigido; testes aprovados |
| 27 | Contagens nominais apesar de NaN | src/agio/analise.py; src/agio/relatorio.py | n efetivo por ponto, n nominal e placebo mantidos | test_aud002.py; comparativo_trajetorias.csv | Quatro figuras e 12 CSVs de trajetórias; médias/faixas iguais | Corrigido; testes aprovados |
| 31 | Volume-base USDT rotulado BRL | src/agio/episodio.py; docs/resultados.md | Rótulo USDT e variação percentual conferida | test_aud002.py; episodio_v2.log | 17,1457 → 26,0686 mi USDT; +52,0411% | Corrigido; testes aprovados |

Saídas foram direcionadas a resultados_v2, tratado_v2 e docs/v2 para preservar as referências. Os logs regressoes_antes/depois e hipoteses_antes/depois demonstram os comportamentos antes/depois. As regras aprovadas não foram inseridas retroativamente no pré-registro.
