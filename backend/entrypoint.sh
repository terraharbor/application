#!/bin/sh
set -e

mkdir -p "$STATE_DATA_DIR"
chown -R app:app "$STATE_DATA_DIR"

exec su-exec app "$@"
