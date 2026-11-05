# Decisões autorizadas para a V2 — 02/11/2026

Este registro novo documenta decisões explícitas do pesquisador na conversa AUD-002. Não reescreve docs/pre-registro.md, não modifica V1–V6 nem toma decisões sobre avaliação sequencial.

## AUD-001-21: elegibilidade V1

Autorização: “Exigir pelo menos 10 domésticos e 10 externos”. Contar eventos com CAR válido da lista completa: domésticos=fiscal+político, externos=externo. Zero/grupo ausente, contagem indisponível ou qualquer grupo abaixo de dez gera inconclusivo nas duas decisões; não negativo. Com ambos ≥10, mantém-se o teste conjunto de sinais e máximo dos p-valores. Quando um componente do teste conjunto não é estimável, o p conjunto é ausente, não apenas o p do componente restante. A insuficiência amostral não elimina uma hipótese da família.

## AUD-001-22: hipótese não estimável e Holm

Autorização: manter V5 não estimável, p bruto ausente e valor interno 1 somente como reserva conservadora de sua posição na família de sete. São sempre V1,V2,V3,V4a,V4b,V5,V6. A coluna estimavel identifica disponibilidade do p; p_valor e p_holm de hipótese não estimável ficam ausentes; confirma e confirma_holm ficam inconclusivo. Para as hipóteses estimáveis, o cálculo de Holm usa sete posições, sem excluir a vaga indisponível. O 1 interno não é estatística, estimativa ou evidência observada e não é publicado como p bruto.

Justificativa: manter o tamanho da família registrada evita reduzir silenciosamente os multiplicadores de Holm. Reservar posição no extremo superior não introduz evidência de rejeição; a hipótese não estimável não é rejeitada. A família com sete p-valores observados mantém resultados idênticos à implementação anterior. Essa política não corrige seleção exploratória, dependência temporal ou a regra sequencial, fora do escopo autorizado.

## Versionamento de saídas

Resultados originais: dados/resultados e docs/figuras, preservados; cópia histórica completa em auditorias/AUD-002/baseline_original. Lista original: dados/manual/eventos.csv. Lista V2: dados/manual/eventos_v2.csv. Resultados corrigidos: dados/resultados_v2. Figuras/tabelas corrigidas: docs/v2. Proveniência e comparação por artefato: auditorias/AUD-002. Parâmetros estatísticos e dados históricos são preservados.
