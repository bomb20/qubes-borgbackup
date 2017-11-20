#!/usr/bin/env bash

## Local Backup to USB-Drive not supported yet
if [ "$1" == local ]
then
#  REPOSiTORY=/mnt/removable/vincent/borg
else
  REPOSITORY=tombstone:/home/vincent/borg # <- Path to your remote borg-repository
fi

## This is OK, since the Backup-VM is a trusted domain
export BORG_PASSPHRASE="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # <- The passphrase to your remote borg-repository

## The list of exclude-statements is growing... mabe make an extra file for that in the future
borg create -v --stats --progress --compression lz4 --exclude-caches \
  -e 're:.*\/lost\+found' -e */.config/PyBitmessage/messages.dat \
  -e */Downloads -e */tmp $REPOSITORY::'{hostname}-{now:%Y-%m-%d-%H%M%S}' /mnt/homes/

echo "Pruning archives..."
borg prune -v --list $REPOSITORY --prefix '{hostname}-' \
    --keep-within=2d --keep-daily=7 --keep-weekly=4 --keep-monthly=12 --keep-yearly=100

exit 0
