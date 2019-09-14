#!/bin/bash
#
# IMPORTANT: Make sure there is at least 30 GB disk space available.
#
# Automatically visits each URL 10 times and records network traffic for a
# duration of 10s each access.
#
# Make sure you have root privileges before running this script.
# Have Firefox open to a blank tab for slower computers/VMs.

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

for url_idx in {0..9}; do
  [ -d ${url_idx} ] || mkdir ${url_idx}
  for access_num in {0..9}; do
    sudo tcpdump -U -i any -w ./${url_idx}/${access_num}.pcap &> /dev/null &
    tcp_pid=$!
    sleep 2
    firefox ${urls[$url_idx]} &
    ffx_pid=$!
    sleep 10
    wmctrl -a firefox && xdotool key Ctrl+w
    #kill $ffx_pid
    sleep 3
    sudo kill $tcp_pid
  done
done

unset urls
unset url_idx
unset access_num
unset tcp_pid
unset ffx_pid
