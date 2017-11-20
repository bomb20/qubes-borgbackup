#!/usr/bin/env python3

import os
import string

vms = ['foo', 'bar', 'baz'] # <- List of the VM's you want to backup. Currently max. 18 entries are supported due to poorly documented virtual-blockdevice-identifyer policy

if len(vms) > 18:
  quit()

os.system("qvm-start backup")

for vm in vms:
  os.system("qvm-shutdown --wait " + vm)

letters = string.ascii_lowercase[8:]

idents = {}

## Usually you would do a 'for k,v in idents.items():'-loop, but somehow the Order in wich the blockdevices are assigned plays a role in not crashing
for i in range(len(vms)):
  idents[letters[i]] = vms[i]

for i in range(len(vms)):
  os.system("qvm-block -A -f xvd" + letters[i] + " backup dom0:/var/lib/qubes/appvms/" + idents[letters[i]] + "/private.img")

os.system("qvm-run backup 'sudo mkdir /mnt/images'")
os.system("qvm-run backup 'sudo mkdir /mnt/homes'")
for i,vm in idents.items():
  os.system("qvm-run backup 'sudo mkdir /mnt/images/" + vm + "'")
  os.system("qvm-run backup 'sudo mount -o ro /dev/xvd" + i + " /mnt/images/" + vm + "'")
  os.system("qvm-run backup 'sudo mkdir /mnt/homes/" + vm + "'")
  os.system("qvm-run backup 'sudo mount -o bind /mnt/images/" + vm + "/home/user /mnt/homes/" + vm + "'")


os.system("qvm-run --pass-io backup 'terminator -x ~/backup.sh && poweroff'") # <- command to run in the backup-vm (usually your backup script). 
# Make sure you power down the Backup-vm afterwards to guarantee the VM's private images are not assighed to it anymore
