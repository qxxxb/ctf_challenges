#!/usr/bin/env bash

rm -f dist/casino.zip
cd deploy
mkdir casino
rsync -avzP . casino --exclude='casino' --exclude='*node_modules*' --exclude=".env"

cd casino
zip -r casino.zip .
mv casino.zip ../..
cd ../..
rm -rf deploy/casino

mkdir -p dist
mv casino.zip dist
