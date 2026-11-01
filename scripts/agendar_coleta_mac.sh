#!/bin/bash
# Agenda a coleta semanal no Mac (launchd): toda segunda-feira às 20h.
# Se o Mac estiver dormindo nesse horário, roda quando ele acordar.
#
# Instalar:   ./scripts/agendar_coleta_mac.sh
# Remover:    launchctl unload ~/Library/LaunchAgents/br.agio.coleta-semanal.plist
#             rm ~/Library/LaunchAgents/br.agio.coleta-semanal.plist

set -eu
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
PLIST="$HOME/Library/LaunchAgents/br.agio.coleta-semanal.plist"
chmod +x "$RAIZ/scripts/coleta_semanal.sh"
mkdir -p "$HOME/Library/LaunchAgents" "$RAIZ/dados/logs"

cat >"$PLIST" <<PL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>br.agio.coleta-semanal</string>
  <key>ProgramArguments</key>
  <array><string>$RAIZ/scripts/coleta_semanal.sh</string></array>
  <key>StartCalendarInterval</key>
  <dict><key>Weekday</key><integer>1</integer><key>Hour</key><integer>20</integer><key>Minute</key><integer>0</integer></dict>
  <key>StandardOutPath</key><string>$RAIZ/dados/logs/launchd.log</string>
  <key>StandardErrorPath</key><string>$RAIZ/dados/logs/launchd.log</string>
</dict>
</plist>
PL

launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"
echo "Coleta agendada: toda segunda às 20h."
echo "Conferir: launchctl list | grep agio"
echo "Logs em: $RAIZ/dados/logs/"
