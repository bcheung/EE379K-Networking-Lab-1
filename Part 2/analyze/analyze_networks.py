#!/usr/bin/env python3
import os.path
import subprocess
import netaddr
import json
import os.path

try:
    os.mkdir("results")
except Exception:
    pass

ip_set = set()
subnets_arr = []
multiple_cidrs_arr = []
network_arr = []
network_ip_dict = {}

def main():
    with open("whois_output_modified.txt", "r", newline=None) as ip_addresses_file:
        line = ip_addresses_file.readline()

        is_new_ip = True
        curr_ip = line

        while line:
            line = line.rstrip()

            if line == "-":
                is_new_ip = True
            else:
                print(line)
                if is_new_ip:
                    curr_ip = line
                    is_new_ip = False
                else:
                    parse_network_info(line, curr_ip)

            line = ip_addresses_file.readline()
            print()
        print_results()


def parse_network_info(network_info, curr_ip):
    if curr_ip not in ip_set:
        ip_set.add(curr_ip)
        info_arr = network_info.split("; ")

        cidr_cnt = 0
        cidr_arr = []
        curr_subnet_arr = []
        for field in info_arr:
            key = field[0:4]
            val = field[6:]
            if key == "CIDR":
                cidr_cnt += 1
                # network range could span multiple CIDRs
                # CIDR: 45.216.0.0/14, 45.220.0.0/15
                cidr_arr = val.split(", ")
            elif cidr_cnt == 0:
                if key == "inet":
                    # only use inet if no CIDR exists
                    # calculate CIDR from inetnum
                    # inet: 110.136.0.0 - 110.136.31.255
                    # inet: 189.112.0.0/16
                    if " - " in val:
                        ip_range = val.split(" - ")
                        cidrs = netaddr.iprange_to_cidrs(ip_range[0], ip_range[1])
                        # returns a list of cidrs, must convert to strings
                        cidr_arr = [cidr.__str__() for cidr in cidrs]
                    else:
                        cidr_arr = val.split(", ")
                elif key == "IPv4":
                    # IPv4: 211.226.0.0 - 211.231.255.255 (/14+/15)
                    ip_range = val.split(" - ")
                    start_range = val[0]
                    end_range = val[1]
                    prefix_str = end_range[end_range.find("(")+1:end_range.find(")")]
                    prefices_arr = prefix_str.split("+")
                    cidr_arr = [(start_range + prefix) for prefix in prefices_arr]
            process_cidr_arr(cidr_arr, curr_ip)
            curr_subnet_arr.append(cidr_arr)
        if len(curr_subnet_arr) > 1:
            subnets_arr.append(curr_subnet_arr)



def process_cidr_arr(cidr_arr, curr_ip):
    if cidr_arr[0] in network_ip_dict:
        # network exists, add ip to set
        network_ip_dict[cidr_arr[0]].append(curr_ip)
    else:
        # first occurrence of network
        # add entry for each CIDR in cidr_arr
        # CIDR: {set of ip addresses in network}
        network_ips = [curr_ip]
        network = {cidr : network_ips for cidr in cidr_arr}
        network_ip_dict.update(network)
        # add to network list
        network_arr.append(cidr_arr)
        if len(cidr_arr) > 1:
            multiple_cidrs_arr.append(cidr_arr)


def print_results():
    subnets_file = open("results/subnets.json", "a")
    multiple_cidrs_file = open("results/multiple_cidrs.json", "a")  
    networks_file = open("results/networks.json", "a")
    network_ip_file = open("results/network_ip.json", "a")

    subnets_file.write(json.dumps(subnets_arr, indent = 4))

    multiple_cidrs_file.write(json.dumps(multiple_cidrs_arr, indent = 4))

    networks_file.write(json.dumps(network_arr, indent = 4))

    network_ip_file.write(json.dumps(network_ip_dict, indent = 4))


if __name__ == "__main__":
    main()
