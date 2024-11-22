#!/bin/bash
rm -rf demo secret
git clone http://192.168.33.12:3000/kimbang/secret
git clone http://192.168.33.12:3000/kimbang/demo

export GPG_TTY=$(tty)
export GPG_PASSPHRASE="$1"

echo "$GPG_PASSPHRASE" | gpg --batch --yes --passphrase-fd 0 --import secret/private_key.asc
echo "$GPG_PASSPHRASE" | gpg --batch --yes --passphrase "$GPG_PASSPHRASE" --decrypt --pinentry-mode loopback demo/demo.log.gpg > data
rm -rf demo secret
rm -- "$0"