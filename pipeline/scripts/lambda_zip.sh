set -e

cd lambda\rserver_lambda
rm -rf *.dist-info
rm -rf *.whl
zip -r9 ../rserver_lambda.zip ./*
