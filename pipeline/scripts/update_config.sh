set -e

cd infra

rm appsettings.json

if [ "$1" == "dev" ]; then
    rm appsettings.nonprd.json
fi
if [ "$1" == "nonprd" ]; then
    rm appsettings.dev.json
fi
if [ "$1" == "prd" ]; then
    rm appsettings.nonprd.json
    rm appsettings.dev.json
fi

mv appsettings.$1.json appsettings.json

