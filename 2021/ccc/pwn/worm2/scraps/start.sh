#!/usr/bin/env bash
addgroup user0
addgroup user1
addgroup user2
adduser --no-create-home --disabled-password --gecos "" --ingroup user0 user0
adduser --no-create-home --disabled-password --gecos "" --ingroup user1 user1
adduser --no-create-home --disabled-password --gecos "" --ingroup user2 user2

cd app
alias l="ls -lah"

rm -rf door0

mkdir -p door0
chown user0:user1 door0
chmod 550 door0

cd door0
gcc -o key -DID=1001 /app/app.c
chown user1:user0 key
chmod 4550 key
setcap cap_setuid,cap_setgid=ep ./key

mkdir -p door0
chown user1:user2 door0
chmod 550 door0

cd door0
gcc -o key -DID=1002 /app/app.c
chown user2:user1 key
chmod 4555 key
setcap cap_setuid,cap_setgid=ep ./key
cd ..

mkdir -p door1
chown user1:user2 door1
chmod 550 door1

cd door1
gcc -o key -DID=1002 /app/app.c
chown user2:user1 key
chmod 4555 key
setcap cap_setuid,cap_setgid=ep ./key
cd ..
