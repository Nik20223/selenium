#!/bin/sh
#
# Runs from /tmp/init-scripts after the installer finished and right before
# Apache starts; docker_run.sh executes every file in that directory.
#
# A fresh install with PS_COUNTRY=us activates a single currency (USD), and the
# classic theme then renders no currency selector at all - which is exactly the
# block the currency tests switch. The old hand-made stand had the Euro added by
# hand, so seed it here to keep the shop the tests expect.
set -e

EURO_ID=$(mysql --host="$DB_SERVER" --user="$DB_USER" --password="$DB_PASSWD" \
    --database="$DB_NAME" --batch --skip-column-names \
    --execute="SELECT id_currency FROM ps_currency WHERE iso_code = 'EUR' LIMIT 1")

if [ -n "$EURO_ID" ]; then
    echo "* Euro currency is already present, nothing to seed"
    exit 0
fi

# The heredoc is quoted so the shell leaves the backticks around the reserved
# column name `precision` alone, which is why the table prefix is written out
# instead of coming from DB_PREFIX (`ps_` in docker-compose.yml).
mysql --host="$DB_SERVER" --user="$DB_USER" --password="$DB_PASSWD" \
    --database="$DB_NAME" <<'SQL'
SET @id_currency = (SELECT COALESCE(MAX(id_currency), 0) + 1 FROM ps_currency);

INSERT INTO ps_currency
    (id_currency, name, iso_code, numeric_iso_code, `precision`, conversion_rate, deleted, active, unofficial, modified)
VALUES
    (@id_currency, 'Euro', 'EUR', '978', 2, 0.920000, 0, 1, 0, 0);

INSERT INTO ps_currency_lang (id_currency, id_lang, name, symbol, pattern)
VALUES (@id_currency, 1, 'Euro', UNHEX('E282AC'), '');

INSERT INTO ps_currency_shop (id_currency, id_shop, conversion_rate)
VALUES (@id_currency, 1, 0.920000);
SQL

echo "* Euro currency seeded"
