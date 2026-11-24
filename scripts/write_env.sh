#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../../pf-common/scripts/write_env_common.sh
source "$SCRIPT_DIR/../../pf-common/scripts/write_env_common.sh"

ENV_FILE="${ENV_FILE:-.env}"
PAYROLL_ENV="${PAYROLL_ENV:-development}"
PF_DATABASE_URL="${PF_DATABASE_URL:-postgresql+asyncpg://pf_db:pf_db@localhost:5432/pf_db}"
PAYROLL_LOG_LEVEL="${PAYROLL_LOG_LEVEL:-INFO}"
PF_SVC_REFERENCE_URL="${PF_SVC_REFERENCE_URL:-http://localhost:8001}"
PF_SVC_REFERENCE_API_KEY="${PF_SVC_REFERENCE_API_KEY:-change-me-before-use}"
PF_SVC_INCOME_API_KEY="${PF_SVC_INCOME_API_KEY:-change-me-before-use}"
CORPORATIVE_PIP_INDEX="${CORPORATIVE_PIP_INDEX:-}"
CORPORATIVE_NPM_REGISTRY="${CORPORATIVE_NPM_REGISTRY:-}"
CORPORATIVE_PROXY="${CORPORATIVE_PROXY:-}"

{
  printf 'PAYROLL_ENV=%s\n' "$PAYROLL_ENV"
  printf '# Database managed by pf-db (shared with pf-svc-reference)\n'
  printf 'PF_DATABASE_URL=%s\n' "$PF_DATABASE_URL"
  printf 'PAYROLL_LOG_LEVEL=%s\n' "$PAYROLL_LOG_LEVEL"
  printf 'PF_SVC_REFERENCE_URL=%s\n' "$PF_SVC_REFERENCE_URL"
  printf '# API key sent as X-API-Key header to pf-svc-reference -- must match pf-svc-reference own\n'
  printf '# PF_SVC_REFERENCE_API_KEY, which is always enforced (no no-auth mode).\n'
  printf 'PF_SVC_REFERENCE_API_KEY=%s\n' "$PF_SVC_REFERENCE_API_KEY"
  printf '\n# API key that clients must supply as X-API-Key header to access this service.\n'
  printf 'PF_SVC_INCOME_API_KEY=%s\n' "$PF_SVC_INCOME_API_KEY"
  pf_corporate_tooling_env_block "$CORPORATIVE_PIP_INDEX" "$CORPORATIVE_NPM_REGISTRY" "$CORPORATIVE_PROXY"
} > "$ENV_FILE"

printf '%s\n' "$ENV_FILE"
