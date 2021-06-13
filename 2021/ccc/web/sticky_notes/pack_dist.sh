#!/usr/bin/env bash

rm -f dist/sticky_notes.zip
cd deploy
mkdir sticky_notes
rsync -avzP . sticky_notes --exclude='sticky_notes' --exclude='*node_modules*' --exclude='*__pycache__*' --exclude=".env"
sed -i 's/CCC{.*}/CCC{this_is_a_fake_flag}/g' sticky_notes/Dockerfile

cd sticky_notes
zip -r sticky_notes.zip .
mv sticky_notes.zip ../..
cd ../..
rm -rf deploy/sticky_notes

mkdir -p dist
mv sticky_notes.zip dist
