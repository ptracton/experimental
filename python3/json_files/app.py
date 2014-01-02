#! /usr/bin/env python3

#import json
#import configparser
import AppJSON
import FlowEngine

if __name__ == '__main__':
#    f = open("app.json")
#    foo = json.load(f)
#    for k,v in foo.items():
#        print (k,v)

    decoder = AppJSON.AppJSONDecoder(file_name = "app.json")
    engine = FlowEngine.FlowEngine(decoder.GetDictionary('flow_steps'), decoder.GetDictionary('flow'))
    engine.Execute()

#    config = configparser.ConfigParser()
#    config.read("app.cfg")
#    print(config.sections())
#    print (config['Projects']['recent_projects'])
    pass
