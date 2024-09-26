#!/bin/sh
#
# Takes one positional argument
#   1: the absolute path to the thing to store onto drobo
#

path_from=${1}
logfile=/etc/drobo/drobo_log.csv

if [ ! -e ${path_from} ] ; then
	echo "${path_from} does not exist.  Check your path name as typed."
	exit
fi

DROBOCMD="rsync -tlrR ${path_from} root@rushmore:/mnt/drobo/"
TIMESTAMP=`date -I'seconds'`
ACTION="store"
ADMIN=${USER}
IPADDRESS=`nslookup ${HOSTNAME} | grep Address | tail -n1 | awk '{print $2}'`

ssh root@rushmore "touch ${logfile}"
ssh root@rushmore "echo \"${TIMESTAMP},${ACTION},${path_from},${ADMIN},${IPADDRESS},${DROBOCMD}\" >> ${logfile}"

eval ${DROBOCMD}