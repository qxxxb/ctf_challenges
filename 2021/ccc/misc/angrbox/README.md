# angrbox

Challenge:
```
[*] Write me a program that:
[*] - Takes 4 uppercase characters in argv
[*] - Verifies the 4 character key and returns 0 if correct
[*] - If I find the key, YOU LOSE
```

## Deployment notes

To pack `angrbox.zip` do `./pack_dist.sh` (should already be packed tho since
`angrbox.zip` is included in the git repo for convenience)

This challenge is tuned to accept a maximum of 4 concurrent connections. Excess
connections are queued until another exits (max 3 min per connection).

> If the challenge is under-resourced it's possible to cheese the flag, but I
> tried to make that impossible as long as the container is given enough RAM.

For 4 concurrent connections, the challenge needs at least 1 GB of RAM.

If we want to increase or decrease the amount of RAM and CPU given to this
container, it's important to change the nsjail configs as well.

Currently `jails/angr.cfg` is set to:
```
cgroup_cpu_ms_per_sec: 210
cgroup_mem_max: 228170137
```

Because
```
(210 * 4) / 1000 = 0.84
  4 workers => 84% CPU
(228170137 * 4) / (1024 * 1024 * 1024) = 0.85
  4 workers => 85% RAM
```
