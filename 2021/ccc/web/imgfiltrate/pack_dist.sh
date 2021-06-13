#!/usr/bin/env bash

rm -f dist/imgfiltrate.zip
cd deploy
mkdir imgfiltrate
rsync -avzP . imgfiltrate --exclude='imgfiltrate' --exclude='*node_modules*' --exclude='*dist.zip' --exclude='*.env'
rm imgfiltrate/app/imgs/flag.png
cp ../resources/fake_flag.png imgfiltrate/app/imgs/flag.png

cd imgfiltrate
zip -r imgfiltrate.zip .
mv imgfiltrate.zip ../..
cd ../..
rm -rf deploy/imgfiltrate

mkdir -p dist
mv imgfiltrate.zip dist
