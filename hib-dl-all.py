#!/usr/bin/env python
import humblebundle
import argparse
import os
import subprocess

parser = argparse.ArgumentParser(description='downloads your whole humble bundle library.')
parser.add_argument('-u', metavar='user@mail.com', help='your humblebundle.com username', dest='username')
parser.add_argument('-p', metavar='hunter2', help='your humblebundle.com password', dest='password')
# not yet implemented
#parser.add_argument('-k', metavar='KEY', help='humble key for a purchase or bundle', dest='keys', nargs='*')
parser.add_argument('-d', metavar='DIRECTORY', help='your games will be saved here', dest='directory', default='.')

args = parser.parse_args()
#if(args.keys == None and args.username == None):
if(args.username == None):
    parser.print_help()
    exit(1)

os.chdir(args.directory)

client = humblebundle.HumbleApi()
client.login(args.username, args.password)

order_list = client.order_list()
for order in order_list:
    if order.subproducts != None:
        for subproduct in order.subproducts:
            if subproduct.downloads != None:
                for download in subproduct.downloads:
                    for download_struct in download.download_struct:
                        url = download_struct.url.web
                        if url != None:
                           filename = url.split("/")[3].split("?")[0]
                           if not os.path.isfile(filename):
                               subprocess.run(["wget", "-c", "-O", filename, url]).check_returncode()
