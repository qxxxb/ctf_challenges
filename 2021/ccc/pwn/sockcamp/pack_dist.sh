#!/usr/bin/env bash

rm -f dist/sockcamp.zip

cd deploy
mkdir dist
rsync -avzP . dist --exclude='dist' --exclude="initramfs.cpio.gz"
cp ../pre_dist/initramfs.cpio.gz dist/
cp -r ../src dist/

cd dist
zip -r dist.zip .
mv dist.zip ../..
cd ../..
rm -rf deploy/dist

mkdir -p dist
mv dist.zip dist/sockcamp.zip
