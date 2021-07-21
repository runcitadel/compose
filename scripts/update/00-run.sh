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

# Check if $NODE_ROOT/.umbrel-$RELEASE exists, if it does, rename it to $NODE_ROOT/.citadel-$RELEASE
if [ -d "$NODE_ROOT/.umbrel-$RELEASE" ]; then
    echo "Migrating from Umbrel..."
    echo "Your Umbrel will now be turned into a Citadel"
    echo "Please contact the Citadel team if anything goes wrong during the update"
    echo "Waiting 5 seconds, then the migration will start"
    sleep 5
    mv "$NODE_ROOT/.umbrel-$RELEASE" "$NODE_ROOT/.citadel-$RELEASE"
fi

# Make sure any previous backup doesn't exist
if [[ -d "$NODE_ROOT"/.citadel-backup ]]; then
    echo "Cannot install update. A previous backup already exists at $NODE_ROOT/.umbrel-backup"
    echo "This can only happen if the previous update installation wasn't successful"
    exit 1
fi

echo "Installing Citadel $RELEASE at $NODE_ROOT"

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
    --include-from="$NODE_ROOT/.citadel-$RELEASE/scripts/update/.updateinclude" \
    --exclude-from="$NODE_ROOT/.citadel-$RELEASE/scripts/update/.updateignore" \
    "$NODE_ROOT"/ \
    "$NODE_ROOT"/.citadel-backup/

echo "Successfully backed up to $NODE_ROOT/.citadel-backup"
