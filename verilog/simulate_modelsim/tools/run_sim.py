#! /usr/bin/env python3

import json
import os
import shlex
import subprocess
import sys
#import time

def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

if __name__ == '__main__':
    
    json_file = "../../configurations/simulate_modelsim.json"
    try: 
        f = open(json_file, "r")        
        json_data = json.load(f)
    except:
        print("Failed to open %s" % (json_file))
        sys.exit(-1)

    steps = json_data['flow_steps'].values()
    for step in steps:
        print("Running Step: %s " % step)
        executable = json_data['flow'][step]['executable']
        arguments  = json_data['flow'][step]['arguments']
        executable = which(executable)
        #print(executable)
        if (arguments == None):
            command = executable
        else:
            command = executable +" " +arguments

        print(command)
        command = shlex.split(command)
        p = subprocess.Popen(command)
