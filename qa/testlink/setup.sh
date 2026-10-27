#!/usr/bin/env bash
# Starts TestLink 1.9.20 for SECJ3343 on http://localhost:8090 (macOS + Docker Desktop).
set -euo pipefail
cd "$(dirname "$0")"

command -v docker >/dev/null || { echo "Install Docker Desktop first: brew install --cask docker-desktop, then open it"; exit 1; }
docker info >/dev/null 2>&1 || { open -a Docker; echo "Waiting for Docker Desktop..."; until docker info >/dev/null 2>&1; do sleep 3; done; }

if [ ! -d app ]; then
  git clone -q --depth 1 -b testlink_1_9_20_fixed https://github.com/TestLinkOpenSourceTRMS/testlink-code.git app
  rm -rf app/.git
fi
# Generate a genuinely empty TestLink database. Never copy another group's seed.
mkdir -p seed
python3 - <<'PY'
from pathlib import Path
for number, name in enumerate(('testlink_create_tables.sql', 'testlink_create_default_data.sql', 'testlink_create_udf0.sql'), 1):
    source = Path('app/install/sql/mysql') / name
    text = source.read_text().replace('/*prefix*/', '').replace('YOUR_TL_DBNAME', 'testlink')
    (Path('seed') / f'{number:02d} {name}').write_text(text)
PY
# gist edits (paths), API typo fix, DB config, report header
cp -R overlay/ app/
mkdir -p app/logs app/upload_area app/lib/ajax/logs app/gui/templates_c
chmod -R 777 app/logs app/upload_area app/lib/ajax/logs app/gui/templates_c

docker compose up -d --build
PORT=${TESTLINK_PORT:-8090}
echo "Waiting for TestLink..."
until curl -sf -o /dev/null "http://localhost:$PORT/login.php"; do sleep 3; done
until docker compose exec -T db mariadb -uroot -proot -N testlink -e "SELECT 1 FROM users LIMIT 1" >/dev/null 2>&1; do sleep 3; done
python3 -I scripts/bootstrap.py
echo "TestLink ready: http://localhost:$PORT (admin/admin; aland/aland; lanya/lanya; mhammedazad/mhammedazad; ahmed/ahmed; rasan/rasan)"
