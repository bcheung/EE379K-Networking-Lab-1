#!/bin/bash
#
# Automatically summarizes generated .pcap files from auto_collect.sh,
# dumping filename,num_packets,avg_packet_length into into
# <access_method>_packet_info.csv, where <access_method> is passed in
# as the first parameter.
# e.g. Firefox=ffx, Tor=tor, VPN=vpn, etc.

urls=(
  'https://en.wikipedia.org/wiki/Cat'
  'https://en.wikipedia.org/wiki/Dog'
  'https://en.wikipedia.org/wiki/Egress_filtering'
  'http://web.mit.edu/'
  'http://www.unm.edu/'
  'https://cmu.edu/'
  'https://www.berkeley.edu/'
  'https://www.utexas.edu/'
  'https://www.asu.edu/'
  'https://www.utdallas.edu/'
)

FILE="./${1:+${1}_}packet_info.csv"

[ -f $FILE ] && rm $FILE
touch $FILE

for dir in {0..9}; do
  echo ${urls[$dir]} >> $FILE
  for f in {0..9}; do
    capinfos -zcrmT ./${dir}/${f}.pcap >> $FILE
  done
  echo >> $FILE
done

unset FILE
unset urls
unset dir
unset f
