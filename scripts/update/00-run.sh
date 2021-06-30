#!/usr/bin/env bash
set -euo pipefail

RELEASE=$1
NODE_ROOT=$2

echo
echo "======================================="
echo "=============== UPDATE ================"
echo "======================================="
echo "========= Stage: Pre-update ==========="
echo "======================================="
echo

# Make sure any previous backup doesn't exist
if [[ -d "$NODE_ROOT"/.umbrel-backup ]]; then
    echo "Cannot install update. A previous backup already exists at $NODE_ROOT/.umbrel-backup"
    echo "This can only happen if the previous update installation wasn't successful"
    exit 1
fi

echo "Installing Umbrel $RELEASE at $NODE_ROOT"

# Update status file
cat <<EOF > "$NODE_ROOT"/statuses/update-status.json
{"state": "installing", "progress": 20, "description": "Backing up", "updateTo": "$RELEASE"}
EOF

# Fix permissions
echo "Fixing permissions"
chown -R 1000:1000 "$NODE_ROOT"/

# Backup
echo "Backing up existing directory tree"

rsync -av \
    --include-from="$NODE_ROOT/.umbrel-$RELEASE/scripts/update/.updateinclude" \
    --exclude-from="$NODE_ROOT/.umbrel-$RELEASE/scripts/update/.updateignore" \
    "$NODE_ROOT"/ \
    "$NODE_ROOT"/.umbrel-backup/

echo "Successfully backed up to $NODE_ROOT/.umbrel-backup"
