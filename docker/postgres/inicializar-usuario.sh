#!/bin/sh
set -eu

case "$POSTGRES_DB:$APP_DB_USER" in
    seguranca_alimentar_dev:seguranca_dev)
        ;;
    seguranca_alimentar_test:seguranca_test)
        ;;
    *)
        echo "Use um par de banco e usuário local descrito no README." >&2
        exit 1
        ;;
esac

psql --no-psqlrc --set=ON_ERROR_STOP=1 --username=postgres --dbname="$POSTGRES_DB" <<'SQL'
\getenv app_user APP_DB_USER
\getenv app_password APP_DB_PASSWORD
\getenv app_database POSTGRES_DB
CREATE ROLE :"app_user" LOGIN PASSWORD :'app_password';
ALTER DATABASE :"app_database" OWNER TO :"app_user";
SQL

if [ "$APP_DB_USER" = 'seguranca_test' ]; then
    psql --no-psqlrc --set=ON_ERROR_STOP=1 --username=postgres --dbname=postgres \
        --command='ALTER ROLE seguranca_test CREATEDB;'
fi
