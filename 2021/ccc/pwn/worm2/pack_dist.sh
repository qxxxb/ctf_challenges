#!/usr/bin/env bash

rm -f dist/worm2.zip
cd deploy
mkdir dist
rsync -avzP . dist --exclude='dist'
sed -i 's/CCC{.*}/CCC{this_is_a_fake_flag}/g' dist/instance/flag.txt

cd dist
zip -r dist.zip .
mv dist.zip ../..
cd ../..
rm -rf deploy/dist

mkdir -p dist
mv dist.zip dist/worm2.zip
