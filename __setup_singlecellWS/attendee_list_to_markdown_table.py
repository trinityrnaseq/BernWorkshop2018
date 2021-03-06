#!/usr/bin/env python
# encoding: utf-8

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import os, sys, re
import logging
import argparse
import subprocess

reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger(__name__)

rstudio_user_port_default = 10001

def main():

    parser = argparse.ArgumentParser(description="instantiate user spaces", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("--ip_addr", type=str, required=True, nargs='+', help="IP address for server")
    parser.add_argument("--attendee_list", type=str, required=True, help="attendee list file")

    parser.add_argument("--user_id_start", type=int, default=1, help="index to start user IDs (ex. 1)")
    
    parser.add_argument("--rstudio_base_port", type=int, default=rstudio_user_port_default, help="base port for apache")
        
    args = parser.parse_args()
    
    rstudio_user_port = args.rstudio_base_port
    
    ip_addr_list = args.ip_addr
    num_ip_addr = len(ip_addr_list)

    
    attendee_list = []
    user_id = args.user_id_start
    with open(args.attendee_list) as f:
        for attendee_name in f:
            attendee_list.append(attendee_name)

    attendee_list.sort()
    num_attendees = len(attendee_list)
    students_per_ip = num_attendees / num_ip_addr

    prev_ip_bin = 0

    print("|" + "|".join(["Attendee", "RStudio"]) + "|")
    print("|" + "|".join(["-------------", "----------------"]) + "|")
    
    for i, attendee in enumerate(attendee_list):
        
        ip_bin = int(i / students_per_ip)
        if ip_bin != prev_ip_bin:
            # reset
            rstudio_user_port = rstudio_user_port_default
            prev_ip_bin = ip_bin
        
        ip_addr = ip_addr_list[ip_bin]

        attendee_name = attendee.rstrip()
        print("|" + "|".join([attendee_name,
                             "[rstudio](" + url_maker(ip_addr, rstudio_user_port) + ")"]
                             ) + "|")
        
        rstudio_user_port += 1

        user_id += 1
    

    
    sys.exit(0)


def url_maker(ip_addr, port_num):

    return("http://" + ip_addr + ":" + str(port_num))



####################
 
if __name__ == "__main__":
    main()
