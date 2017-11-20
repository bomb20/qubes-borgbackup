This is just a set of scripts to perform backups of your qubes-vm's with
borgbackup.

The script powers off all the important vm's, mounts their private.img-file to
a trusted backup-vm amd performs a borgbackup-backup over all the
home-folders.

CAUTION: Read the code and adapt to your needs before first use. I wrote this just for my personal use
and didn't have the time to make things configurable yet.


