#! /usr/bin/env python3

import sys
import argparse
import json
import os

if __name__ == '__main__':
    print ("\n\nRunning Simulation")

    ##
    ## Process the command line options
    ## 
    parser = argparse.ArgumentParser(description="Microblaze Simulation Tools", \
                                     prefix_chars='-+')
      
    parser.add_argument("--simulator",dest="simulator", \
                        action="store",help="Which simulator to use",   \
                        default="isim",required=False)

    parser.add_argument("--debug",dest="debug", \
                        action="store_true",help="Turns on debugging of run_sim.py script",   \
                        default=False,required=False)

    args = vars(parser.parse_args())
    print (args)

    ##
    ## used must choose 1 of the 3 valid simulation tools we can use.  isim is the default
    ## if nothing is specified.
    ##
    if ( (args['simulator'] != 'isim') and  
         (args['simulator'] != 'irun') and  
         (args['simulator'] != 'iverilog') ):
        print ("Invalid simulator chosen! %s \n" % (args['simulator']))

    ##
    ## Set up using  ISIM
    ## 
    if (args['simulator'] == 'isim'):
        print ("Using ISIM")
        json_file = "../../tools/simulate_isim.json"

    ##
    ## Set up using  IRUN
    ## 
    if (args['simulator'] == 'irun'):
        print ("Using IRUN")
        json_file = "../../tools/simulate_irun.json"

    ##
    ## Set up using  IVERILOG
    ## 
    if (args['simulator'] == 'iverilog'):
        print ("Using IVERILOG")
        json_file = "../../tools/simulate_iverilog.json"


    ##
    ## Open and read JSON file
    ## 
    try: 
        f = open(json_file, "r")    
    except:
        print ("Failed to open %s" % (json_file))
        sys.exit(-1)

    try:
        json_data = json.load(f)
    except:
        print ("Failed to parse JSON file, go to jsonlint.com")
        sys.exit(-1)

    flow_steps = json_data['flow_steps']

    if (args['debug']):
        print (flow_steps)

    for step in sorted(flow_steps.keys()):
        current_step = flow_steps[step]
        print("\nRunning Step: %s " % current_step)
        executable = json_data['flow'][current_step]['executable']
        arguments  = json_data['flow'][current_step]['arguments']
        print(executable)
        print (arguments)
        if (arguments == None):
            command = executable
        else:
            command = executable +" " +str(arguments)

        print(command)
        os.system(command)

    print ("All Done \n\n")
    sys.exit(0)
