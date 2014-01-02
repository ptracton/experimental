#! /usr/bin/env python3

import sys
import os
import os.path
import argparse

list_of_project_dirs = ["/bench/verilog", "/configurations", "/fpga/xilinx", "/fpga/altera", 
                        "/rtl/verilog",  "/sims/tests", "/sims/rtl_sims", "/sims/gate_sims", 
                        "/software/applications", "/software/drivers",
                        "/tools"]

list_of_project_general_files = ["/bench/verilog/testbench.v", "/bench/verilog/timescale.v",
                                 "/bench/verilog/dump.v",]
list_of_project_specific_files = []

def CreateProject(project, directory, debug):
    if (debug):
        print("Project = %s Directory = %s" % (project, directory))

    target_directory = directory + "/" + project
    print(target_directory)

    ##
    ## Make sure this does not already exist, we do not want to over write a existing project
    ##
    if os.path.isdir(target_directory):
        print("\n\nTarget already exists! %s\n" % (target_directory))
        sys.exit(-1)
    
    for dir in list_of_project_dirs:
        os.makedirs(target_directory+dir)

    return

def CreateCore(core, directory, debug):
    if (debug):
        print("Core = %s Directory = %s" % (core, directory))
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--debug", help="Debug this script",
                        action="store_true")

    parser.add_argument("--core", help="Create a new core",
                        action="store")

    parser.add_argument("--project", help="Create a new project",
                        action="store")

    parser.add_argument("--directory", 
                        help="Create the new item in this directory. If not set, assumed to be current directory",
                        action="store")

    args = parser.parse_args()
    if args.debug:
        print(args)

    if (
        ((args.project == None) and (args.core == None)) or
        ((args.project != None) and (args.core != None)) 
        ):
        print("\n\nERROR: Must create either a project OR a core!")
        print("Project = %s Core = %s\n\n" % (args.project, args.core))
        sys.exit(-1)

    if (args.directory):
        target_directory = args.directory
    else:
        target_directory = os.getcwd()

    if args.debug:
        print(target_directory)

    if (args.project != None):
        CreateProject(args.project, target_directory, args.debug)

    if (args.core != None):
        CreateCore(args.core, target_directory, args.debug)

    pass
