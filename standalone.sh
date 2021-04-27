#!/bin/bash

docker run -ti -v /home/marco/dockers/webplayer/src/lib-manager/src/:/app -v /srv/music:/srv/music --env-file ./src/.env --network wp_net --ip 172.15.0.11 lib-manager:test -a "172.15.0.11" -o 20002 -f True