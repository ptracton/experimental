#! /usr/bin/env python3

import json
import string
import sys
if __name__ == "__main__":
    json_file = "./foo.json"
    
    try:
        f = open(json_file, "r")
        json_data = json.load(f)
    except:
        print("Failed to open %s" % (json_file))
        sys.exit(-1)

    steps_dict = json_data["flow_steps"]
    steps_flow = json_data["flow"]
    print (steps_dict)
    for x in sorted(steps_dict.keys()):
        step = steps_dict[x]
        arguments = string.Template(steps_flow[step]["arguments"])
        foo = arguments.safe_substitute(foo="Phil", bar="sleepy", defines="+define+SIM")
        print (foo)
        
