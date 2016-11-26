#!/bin/bash

set -e

pidfile="/tmp/deploy"

# lock it
exec 200>$pidfile
flock -n 200 || ( echo -e "\e[0;31mDeploy script is already running. Aborting . .  $TEXTEND" && exit 1 )
pid=$$
echo $pid 1>&200


if [ -z "$SOCKET_SERVER_ENV" ]
then
        echo -e "\e[0;31mSOCKET_SERVER_ENV is not set. Aborting . .  $TEXTEND"
        exit 1
fi

if [ $SOCKET_SERVER_ENV = "dev" ]
then
        echo -e "\e[0;31mScript should not run from dev. Aborting . .  $TEXTEND"
        exit 1
fi


BUILD=""
if [[ "$1" != "" ]]; then
    BUILD="$1"
fi

TEXTSTART="\n\e[0;33m####"
TEXTEND="\e[0m"
LATEST_BUILD_VAR_FILE=/tmp/pos_latest_"$SOCKET_SERVER_ENV"_build
LATEST_BUILD_FILE=/tmp/pos.deb
TIMESTAMP=$(date '+%Y_%m_%d__%H_%M_%S')


if [ -z "$BUILD" ]
then
        s3cmd get s3://cm.pos.artifacts/pos_latest_"$SOCKET_SERVER_ENV"_build $LATEST_BUILD_VAR_FILE --force
else
        echo "pos.$BUILD.deb" > $LATEST_BUILD_VAR_FILE
fi

BUILD=`cat $LATEST_BUILD_VAR_FILE`

echo -e "$TEXTSTART Starting Deploy for build $BUILD on $SOCKET_SERVER_ENV .. $TEXTEND"

s3cmd get s3://cm.pos.artifacts/"$BUILD" $LATEST_BUILD_FILE --force

echo -e "\n\n\n\n\e[0;32m#######################\n#### Deploy Is Successful\n####################### $TEXTEND"