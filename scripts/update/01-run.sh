#!/usr/bin/env bash
set -euo pipefail

RELEASE=$1
NODE_ROOT=$2

# Only used on Umbrel OS and Citadel OS
SD_CARD_NODE_ROOT="/sd-root${NODE_ROOT}"

echo
echo "======================================="
echo "=============== UPDATE ================"
echo "======================================="
echo "=========== Stage: Install ============"
echo "======================================="
echo

[[ -f "/etc/default/umbrel" ]] && source "/etc/default/umbrel"
[[ -f "/etc/default/citadel" ]] && source "/etc/default/citadel"

IS_MIGRATING=0
# Check if UMBREL_OS is set and CITADEL_OS is not
if [[ -z "$UMBREL_OS" ]] && [[ -n "$CITADEL_OS" ]]; then
    echo "Umbrel OS is being used..."
    echo "Upgrading to Citadel OS..."
    echo "export CITADEL_OS='0.0.1'" > /etc/default/citadel
    IS_MIGRATING=1
    CITADEL_OS='0.0.1'
fi

# Make Umbrel OS specific updates
if [[ ! -z "${CITADEL_OS:-}" ]]; then
    echo 
    echo "============================================="
    echo "Installing on Citadel OS $CITADEL_OS"
    echo "============================================="
    echo
    
    # Update SD card installation
    if  [[ -f "${SD_CARD_NODE_ROOT}/.umbrel" ]] || [[ -f "${SD_CARD_NODE_ROOT}/.citadel" ]]; then
        echo "Replacing ${SD_CARD_NODE_ROOT} on SD card with the new release"
        rsync --archive \
            --verbose \
            --include-from="${NODE_ROOT}/.citadel-${RELEASE}/scripts/update/.updateinclude" \
            --exclude-from="${NODE_ROOT}/.citadel-${RELEASE}/scripts/update/.updateignore" \
            --delete \
            "${NODE_ROOT}/.citadel-${RELEASE}/" \
            "${SD_CARD_NODE_ROOT}/"

        echo "Fixing permissions"
        chown -R 1000:1000 "${SD_CARD_NODE_ROOT}/"
    else
        echo "ERROR: No Umbrel or Citadel installation found at SD root ${SD_CARD_NODE_ROOT}"
        echo "Skipping updating on SD Card..."
    fi

    # This makes sure systemd services are always updated (and new ones are enabled).
    UMBREL_SYSTEMD_SERVICES="${UMBREL_ROOT}/.umbrel-${RELEASE}/scripts/umbrel-os/services/*.service"
    for service_path in $UMBREL_SYSTEMD_SERVICES; do
      service_name=$(basename "${service_path}")
      install -m 644 "${service_path}" "/etc/systemd/system/${service_name}"
      systemctl enable "${service_name}"
    done
fi

cat <<EOF > "$NODE_ROOT"/statuses/update-status.json
{"state": "installing", "progress": 33, "description": "Configuring settings", "updateTo": "$RELEASE"}
EOF

# Checkout to the new release
cd "$NODE_ROOT"/.umbrel-"$RELEASE"

# Configure new install
echo "Configuring new release"
cat <<EOF > "$NODE_ROOT"/statuses/update-status.json
{"state": "installing", "progress": 40, "description": "Configuring new release", "updateTo": "$RELEASE"}
EOF

BITCOIN_NETWORK="mainnet"
[[ -f "$NODE_ROOT/.env" ]] && source "$NODE_ROOT/.env"
NETWORK=$BITCOIN_NETWORK ./scripts/configure

# Stop existing containers
echo "Stopping existing containers"
cat <<EOF > "$NODE_ROOT"/statuses/update-status.json
{"state": "installing", "progress": 70, "description": "Removing old containers", "updateTo": "$RELEASE"}
EOF
cd "$NODE_ROOT"
./scripts/stop


# Overlay home dir structure with new dir tree
echo "Overlaying $NODE_ROOT/ with new directory tree"
rsync --archive \
    --verbose \
    --include-from="$NODE_ROOT/.citadel-$RELEASE/scripts/update/.updateinclude" \
    --exclude-from="$NODE_ROOT/.citadel-$RELEASE/scripts/update/.updateignore" \
    --delete \
    "$NODE_ROOT"/.umbrel-"$RELEASE"/ \
    "$NODE_ROOT"/

echo "Regenerating app config"
cat <<EOF > "$NODE_ROOT"/statuses/update-status.json
{"state": "installing", "progress": 75, "description": "Updating apps...", "updateTo": "$RELEASE"}
EOF
"${NODE_ROOT}/app/apps.py"

# Fix permissions
echo "Fixing permissions"
chown -R 1000:1000 "$NODE_ROOT"/
chmod -R 700 "$NODE_ROOT"/tor/data/*

# Start updated containers
echo "Starting new containers"
cat <<EOF > "$NODE_ROOT"/statuses/update-status.json
{"state": "installing", "progress": 80, "description": "Starting new containers", "updateTo": "$RELEASE"}
EOF
cd "$NODE_ROOT"
./scripts/start

# Make Citadel OS specific post-update changes
if [[ ! -z "${CITADEL_OS:-}" ]]; then

  # Delete unused Docker images on Citadel OS
  echo "Deleting previous images"
  cat <<EOF > "$NODE_ROOT"/statuses/update-status.json
{"state": "installing", "progress": 90, "description": "Deleting previous images", "updateTo": "$RELEASE"}
EOF
  docker image prune --all --force
fi
