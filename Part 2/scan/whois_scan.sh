#!/bin/bash
echo $1 >> results/whois_output.txt
result=$(whois $1 | egrep '^CIDR:|^inetnum:|IPv4 Address ')
if [[ $? != 0 ]]; then
    echo "failed"
else
    echo $result
    echo $result >> results/whois_output.txt
fi
echo "-" >> results/whois_output.txt