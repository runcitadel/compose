#!/usr/bin/env bash
set -euo pipefail

RELEASE=$1
NODE_ROOT=$2

echo
echo "======================================="
echo "=============== UPDATE ================"
echo "======================================="
echo "=========== Stage: Success ============"
echo "======================================="
echo

# Cleanup
echo "Removing backup"
cat <<EOF > "$NODE_ROOT"/statuses/update-status.json
{"state": "installing", "progress": 95, "description": "Removing backup"}
EOF
[[ -d "$NODE_ROOT"/.umbrel-backup ]] && rm -rf "$NODE_ROOT"/.umbrel-backup
[[ -d "$NODE_ROOT"/.citadel-backup ]] && rm -rf "$NODE_ROOT"/.citadel-backup

echo "Successfully installed Umbrel $RELEASE"
cat <<EOF > "$NODE_ROOT"/statuses/update-status.json
{"state": "success", "progress": 100, "description": "Successfully installed Umbrel $RELEASE", "updateTo": ""}
EOF
