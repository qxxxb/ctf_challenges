#!/usr/bin/env bash
mkdir -p /sys/fs/cgroup/{cpu,memory,pids}/NSJAIL
chown inmate /sys/fs/cgroup/{cpu,memory,pids}/NSJAIL
su - inmate -c "nsjail --config $1 -- $2"
