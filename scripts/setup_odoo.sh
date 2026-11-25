#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

docker compose down -v --remove-orphans
docker compose up -d --wait db
docker compose run --rm odoo odoo -d odoo -i sale_management,account --stop-after-init
docker compose up -d --wait odoo
echo "Odoo is ready at http://localhost:8069 (admin / admin)"
