#!/usr/bin/env python3
import os.path
import subprocess

try:
    os.mkdir("results")
except Exception:
    pass

def main():
    # r - read file
    with open('zmap_scan_output.txt', 'r', newline=None) as ip_addresses_file:
        with open("results/failed_ip.txt", "a") as failed_ip:
            with open("results/successful_ip.txt", "a") as successful_ip:
                ip = ip_addresses_file.readline()

                num_ip = 0
                num_successful = 0
                num_failed = 0
                while ip:
                    ip = ip.rstrip()
                    print(ip)
                    num_ip += 1
                    out = subprocess.run(['./whois_scan.sh', ip], stdout=subprocess.PIPE)
                    result = out.stdout.decode("utf-8").rstrip()
                    print(result)
                    if (result == "failed"):
                        failed_ip.write("{}\n".format(ip))
                        num_failed += 1
                    else:
                        successful_ip.write("{}\n".format(ip))
                        num_successful += 1
                    ip = ip_addresses_file.readline()
                    print()
                results_file = open("results/scan_results.txt", "a")
                results_file.write("Total: {}, Successful: {}, Failed: {}".format(num_ip, num_successful, num_failed))


if __name__ == "__main__":
    main()