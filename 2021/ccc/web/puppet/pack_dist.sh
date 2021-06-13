#!/usr/bin/env bash

rm -f dist/puppet.zip
cd deploy
mkdir puppet
rsync -avzP . puppet --exclude='puppet' --exclude='*node_modules*'
rm puppet/frontend/.env
cat > puppet/frontend/.env << EOL
POSTGRES_PASSWORD=not_the_actual_password
FLAG=CCC{this_is_a_fake_flag}
EOL

cd puppet
zip -r puppet.zip .
mv puppet.zip ../..
cd ../..
rm -rf deploy/puppet

mkdir -p dist
mv puppet.zip dist
