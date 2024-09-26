#!/bin/sh
#
# Takes one positional argument
#   1: the absolute path to the thing to restore from drobo
#

path_out=${1}
logfile=/etc/drobo/drobo_log.csv

if [ ! -e ${path_out} ] ; then
	echo "${path_out} does not exist.  Check your path name as typed."
	exit
fi

# Update root@rushmore:/mnt/drobo/ with whatever the mount path end up being on rae's local computer after setting up
DROBOCMD="rsync -tlrR root@rushmore:/mnt/drobo/ ${path_out}"
TIMESTAMP=`date -I'seconds'`
ACTION="store"
ADMIN=${USER}
IPADDRESS=`nslookup ${HOSTNAME} | grep Address | tail -n1 | awk '{print $2}'`

ssh root@rushmore "touch ${logfile}"
ssh root@rushmore "echo \"${TIMESTAMP},${ACTION},${path_out},${ADMIN},${IPADDRESS},${DROBOCMD}\" >> ${logfile}"

eval ${DROBOCMD}