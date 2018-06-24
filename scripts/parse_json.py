#!/bin/env python

import argparse
import sys
import json


def search_key(args, position, key_list):

    # print("args: %s, position: %s, key_list: %s \n" % (type(args), type(position), type(key_list)))
    if isinstance(args, list):
        for i in range(0, len(args)):
            position.append(i)
            key_list = search_key(args[i], position, key_list)

    elif isinstance(args, dict):
        for key in args.keys():
            if key in key_list:
                key_list[key].append(position)
            else:
                key_list[key] = [position]

            position.append(key)
            key_list = search_key(args[key], position,key_list)
            
    else:
        pass

    return key_list


    

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

    key_list = search_key(json_data, [], {})
    
    # if args.ss[count] in json_data.keys():
        
    #     print(json_data[args.ss[count]])
    #     print("type: %s" % type(json_data[args.ss[count]]))
    # else:
    #     print("Not found keyname: %s" % args.ss[count])
    #     quit()
    

        
        
           

    
