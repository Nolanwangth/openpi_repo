#!/usr/bin/env bash
# 薄封装：优先用系统 Python，避免 Conda base 里 OpenSSL 版本不一致导致一运行就崩
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${DIR}/pull_record_by_task.py"
if [[ -x /usr/bin/python3 ]]; then
  exec /usr/bin/python3 "$PY" "$@"
else
  exec python3 "$PY" "$@"
fi
