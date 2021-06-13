#!/usr/bin/env bash

rm -f dist/lord_saturday.zip
cd deploy
mkdir dist
rsync -avzP . dist --exclude='dist' --exclude='*node_modules*'
rm dist/frontend/.env
cat > dist/frontend/.env << EOL
POSTGRES_PASSWORD=not_the_actual_password
EOL

sed -i 's/CCC{.*}/CCC{this_is_a_fake_flag}/g' dist/instance/flag.txt

cd dist
zip -r dist.zip .
mv dist.zip ../..
cd ../..
rm -rf deploy/dist

mkdir -p dist
mv dist.zip dist/lord_saturday.zip
