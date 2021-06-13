#!/usr/bin/env bash

rm -rf dist/angrbox.zip

cd deploy
mkdir angrbox
cp -r docker-compose.yml Dockerfile flag.txt server.py session.py run_jail.sh jails/ jailyard/ ../solve/example_client.py angrbox
sed -i 's/CCC{.*}/CCC{this_is_a_fake_flag}/g' angrbox/flag.txt
cd angrbox
zip -r angrbox.zip .
mv angrbox.zip ../..
cd ../..
rm -rf deploy/angrbox

mv angrbox.zip dist
