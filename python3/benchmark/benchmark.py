#! /usr/bin/env python3

import os
import sys
import configparser
import time


class BenchMarkClass(object):

    def __init__(self, name=None, executable = None, options = None, pre=None, post =None):
        self.start_time = None
        self.end_time = None
        self.run_time = None
        self.project_name = name
        self.executable = executable
        self.options = options
        self.pre_configure = pre
        self.post_execution = post
        return
    def __str__(self):
        string = self.project_name +" "+self.executable+" "+self.options
        return string
    
    def run_pre_configure(self):
        if self.pre_configure != None:
            print("\nPre Configuration: %s" % self.pre_configure)
            os.system(self.pre_configure)
        return
    
    def run_post_execution(self):
        if self.post_execution != None:
            print("\nPost Execution: %s" % self.post_execution)
            os.system(self.post_execution)
            print("\n\n")
        return
    
    def run_benchmark(self):
        if self.executable != None:
            print("\nBenchmark: %s %s" % (self.executable, self.options))
            self.start_time = time.time()
            os.system(self.executable + " " + self.options)
            self.end_time = time.time()
            self.run_time = self.end_time - self.start_time
        return

    def log_results(self, log_file):
        log_file.write(self.project_name+","+str(self.start_time)+","+str(self.end_time)+","+str(self.run_time)+"\n")
        return
    

if __name__ == '__main__':
    
    config = configparser.ConfigParser()
    try:
        config.read('benchmark_config.ini')
    except:
        print("Failed to open config file")
        sys.exit(-1)


    sections_list = config.sections()
    tests_list = config['Benchmark']['tests']
    benchmark_test_list = []
    print (config.sections())
    print (tests_list)
    for x in sections_list:
        if (x in tests_list):            
            print(config.items(x))
            test = BenchMarkClass(name=config[x].get('project_name'),
                                  executable =config[x].get('executable'),
                                  options =config[x].get('options'),
                                  pre =config[x].get('pre_configure'),
                                  post = config[x].get('post_execution')
                                  )
            benchmark_test_list.append(test)
            del(test)

    try:
        log_file = open("benchmark.log", "w")
    except:
        print ("Failed to open log for writing")
        sys.exit(-1)

    log_file.write("Name, Start Time, End Time, Run Time (seconds)\n")
    for t in benchmark_test_list:
        print (t)
        t.run_pre_configure()
        t.run_benchmark()
        t.run_post_execution()
        t.log_results(log_file)
        
    log_file.close()
