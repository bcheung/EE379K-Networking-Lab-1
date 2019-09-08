#!/bin/bash
echo $1 >> whois_output.txt
result=$(whois $1 | egrep '^CIDR:|^inetnum:')
if [[ $? != 0 ]]; then
    echo "failed"
else
    echo $result
    echo $result >> whois_output.txt
fi
echo "-" >> whois_output.txt