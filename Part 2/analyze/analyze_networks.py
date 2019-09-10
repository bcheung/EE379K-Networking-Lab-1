#!/usr/bin/env python3
import os.path
import subprocess
import netaddr
import json
import os.path

ip_set = set()
subnet_set = set()
multiple_cidrs_arr = []
network_ip_cnt_dict = {}
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
                if is_new_ip:
                    curr_ip = line
                    is_new_ip = False
                else:
                    parse_network_info(line, curr_ip)

            line = ip_addresses_file.readline()
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
                    start_range = ip_range[0]
                    end_range = ip_range[1]
                    prefix_str = end_range[end_range.find("(")+1:end_range.find(")")]
                    prefices_arr = prefix_str.split("+")
                    cidr_arr = [start_range + prefix for prefix in prefices_arr]
            process_cidr_arr(cidr_arr, curr_ip)
            curr_subnet_arr.extend(cidr_arr)
        if len(curr_subnet_arr) > 1:
            curr_subnet_arr.sort()
            key = ", ".join(curr_subnet_arr)
            subnet_set.add(key)



def process_cidr_arr(cidr_arr, curr_ip):
    cidr_arr.sort()
    key = ", ".join(cidr_arr)
    if key in network_ip_dict:
        # network exists, add ip to set
        network_ip_dict[key].append(curr_ip)
        network_ip_cnt_dict.update({key: network_ip_cnt_dict[key] + 1})
    else:
        # first occurrence of network
        # add entry for each CIDR in cidr_arr
        # CIDR: {set of ip addresses in network}
        network_ip_arr = [curr_ip]
        network = {key : network_ip_arr}
        network_ip_dict.update(network)
        # add to network list
        network_ip_cnt_dict.update({key: 1})
        if len(cidr_arr) > 1:
            multiple_cidrs_arr.append(key)


def print_results():
    subnets_file = open("results/subnets.json", "a")
    multiple_cidrs_file = open("results/multiple_cidrs.json", "a")
    networks_file = open("results/networks.json", "a")
    network_ip_file = open("results/network_ip.json", "a")

    subnet_arr = list(subnet_set)
    subnets_file.write(json.dumps(subnet_arr, indent = 4))

    multiple_cidrs_file.write(json.dumps(multiple_cidrs_arr, indent = 4))

    networks_file.write(json.dumps(network_ip_cnt_dict, indent = 4))

    network_ip_file.write(json.dumps(network_ip_dict, indent = 4))


if __name__ == "__main__":
    try:
        os.mkdir("results")
        main()
    except Exception:
        print("Must delete results directory to run script")
