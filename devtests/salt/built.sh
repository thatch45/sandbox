#!/bin/bash

makepkg -c -i --asroot --noconfirm
rm -rf /srv/http/pkg/salt-git*
mv salt-git* /srv/http/pkg/
repo-add /srv/http/pkg/salt.db.tar.gz /srv/http/pkg/salt*
