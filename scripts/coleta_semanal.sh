#!/bin/bash
# Coleta semanal da amostra de validação (docs/pre-registro.md).
# Baixa os últimos 10 dias (sobreposição de segurança; a coleta é idempotente),
# recalcula o ágio e grava um log em dados/logs/.
#
# Rodar à mão:   ./scripts/coleta_semanal.sh
# Agendar no Mac: ./scripts/agendar_coleta_mac.sh

set -u
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
cd "$RAIZ" || exit 1
mkdir -p dados/logs
LOG="dados/logs/coleta_$(date +%Y%m%d_%H%M).log"
AGIO="$RAIZ/.venv/bin/agio"

# Início: 10 dias atrás (macOS usa -v; Linux usa -d)
INICIO="$(date -v-10d +%F 2>/dev/null || date -d '10 days ago' +%F)"

{
  echo "=== Coleta semanal: $(date) | início $INICIO ==="
  status=0
  "$AGIO" coletar --inicio "$INICIO" || status=1
  "$AGIO" coletar-horario --inicio "$INICIO" || status=1
  "$AGIO" coletar-controles || status=1
  "$AGIO" calcular || status=1
  if [ "$status" -eq 0 ]; then echo "=== OK ==="; else echo "=== ATENÇÃO: algum passo falhou ==="; fi
} >"$LOG" 2>&1

tail -1 "$LOG"
