#!/bin/env python

import argparse
import sys
import json


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Parse JSON data')
    parser.add_argument('--input', help="Specify JSON file",
                        nargs='?', type=argparse.FileType('r'), required=True,default=sys.stdin)

    parser.add_argument('ss', help="Specify search pattern", nargs='*')

    args = parser.parse_args()
    
    #print(args.searchstring)

    json_data = json.load(args.input)

    print(len(args.ss))

    if (not (len(args.ss) % 2) == 0 ) or len(args.ss) == 0:
        print("Specify searchstring pair")
        quit()

    count = 0

    if args.ss[count] in json_data.keys():
        
        print(json_data[args.ss[count]])
        print("type: %s" % type(json_data[args.ss[count]]))
    else:
        print("Not found keyname: %s" % args.ss[count])
        quit()
    

           

    