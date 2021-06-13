# Double

I saved the flag in a Docker container, but where did Docker actually store it?

Attachments:
- `Ubuntu_5.4.0-62-generic_profile.zip`
- `dump.mem.tar.gz`

## Solution

First set up volatility:

```bash
git clone https://github.com/volatilityfoundation/volatility

echo "Copying dump.mem.tar.xz ..."
cp ../dist/dump.mem.tar.xz volatility

echo "Copying Ubuntu profile ..."
cp ../dist/Ubuntu_5.4.0-62-generic_profile.zip volatility/volatility/plugins/overlays/linux
```

To check that the profile is working, run: `python2 vol.py --info | grep Ubuntu`
This should show the following (ignore the "Failed to import" warnings):
```
Volatility Foundation Volatility Framework 2.6.1
LinuxUbuntu_5_4_0-62-generic_profilex64 - A Profile for Linux Ubuntu_5.4.0-62-generic_profile x64
```

Next extract `dump.mem.tar.xz`:

```bash
cd volatility
echo "Extracting dump.mem.tar.xz, might take a while ..."
tar -xvf dump.mem.tar.xz --checkpoint=.100
echo ""
echo "Done"
```

Now we're set up. To keeps things short, let's make an alias:
```
alias volm="python2 vol.py -f dump.mem --profile=LinuxUbuntu_5_4_0-62-generic_profilex64"
```

First check bash history:
```
$ volm linux_bash
Pid      Name                 Command Time                   Command
-------- -------------------- ------------------------------ -------
    1250 bash                 2021-04-13 06:13:11 UTC+0000   sudo apt-get install virtualbox-guest-x11 curl python3 python3-pip
    1250 bash                 2021-04-13 06:13:11 UTC+0000   vi .Xmodmap
    1250 bash                 2021-04-13 06:13:11 UTC+0000   xmodmap .Xmodmap
    1250 bash                 2021-04-13 06:13:15 UTC+0000   sudo curl https://get.docker.com/ | bash
    1250 bash                 2021-04-13 06:14:50 UTC+0000   sudo -s
    1250 bash                 2021-04-13 06:14:50 UTC+0000   ????????
    1250 bash                 2021-04-13 06:14:50 UTC+0000
   11561 bash                 2021-04-13 06:15:01 UTC+0000   docker run -it alpine:3.7 /bin/sh
```

Only thing interesting is the `docker`. Let's check the processes:
```
$ volm linux_pstree
Name                 Pid             Uid
...
.xfce4-terminal      1245            1000
..bash               1250            1000
...sudo              11560
....bash             11561
.....docker          11568
.packagekitd         1526
.containerd          8757
.dockerd             8876
.containerd-shim     11604
..sh                 11626
...vi                11670
...
```

We see the `docker` command was running in `xfce4-terminal`.
Under `.dockerd` we also see `vi` running inside a shell.

Let's try to get more detail info about these processes:
```
$ volm linux_psaux
...
11560  0      0      sudo -s
11561  0      0      /bin/bash
11568  0      0      docker run -it alpine:3.7 /bin/sh
11604  0      0      /usr/bin/containerd-shim-runc-v2 -namespace moby -id e4af91e1e1bdb71af00437bf9503d5ef97ebf4406343d7778f1b9a52cdaeaa03 -address /run/containerd/containerd.sock
11626  0      0      /bin/sh
11670  0      0      vi secret.txt
...
```

Let's see if it's possible to recover `secret.txt`:
```
$ volm linux_enumerate_files | grep secret
Volatility Foundation Volatility Framework 2.6.1
0xffffa0f6fadd78c8                    289058 /var/lib/docker/overlay2/0302e6c324b486a627e0243c020d8a7d5edd1eab9f186af5d0f6a83b5b82c989/diff/secret.txt
               0x0 ------------------------- /var/lib/docker/overlay2/0302e6c324b486a627e0243c020d8a7d5edd1eab9f186af5d0f6a83b5b82c989-init/diff/secret.txt
               0x0 ------------------------- /var/lib/docker/overlay2/c6010ae8b5857ab4d731cead4147b7d55b6ed8f985d5cbd975cfa529d2d75e30/diff/secret.txt
0xffffa0f6fa676360                    142019 /usr/lib/x86_64-linux-gnu/libsecret-1.so.0.0.0
0xffffa0f6fa99bb40                    289058 /var/lib/docker/overlay2/0302e6c324b486a627e0243c020d8a7d5edd1eab9f186af5d0f6a83b5b82c989/merged/secret.txt
```

Looks like docker did some weird stuff with the file, but let's try and
extract the first one:
```
$ volm linux_find_file -i 0xffffa0f6fadd78c8 -O secret.txt
...
$ cat secret.txt
C C C { d 0 c k 3 r _ i n _ a _ V M }
```

Win
