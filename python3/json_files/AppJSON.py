
import json

class AppJSONDecoder(json.JSONDecoder):

    def __init__(self, file_name = None):
        json.JSONDecoder.__init__(self)
        self.FileName = file_name
        self.JSONData = {}

        try:
            f = open(self.FileName)
            self.JSONData = json.load(f)
        except:
            print("Failed to open %s for reading or JSON" % (self.FileName))
        return

    def GetDictionary(self, name = None):
        if (name == None) or name not in self.JSONData.keys():
            return
        else:
            return self.JSONData[name]

class AppJSONEncoder(json.JSONEncoder):
    def __init__(self):
        json.JSONEncoder.__init__(self)
        pass
