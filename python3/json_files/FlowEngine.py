
class FlowEngine(object):
    def __init__(self, steps = None, flow = None):
        self.FlowSteps = steps
        self.Flow = flow
        return

    def Execute(self):
        for step in self.FlowSteps:
            print(self.FlowSteps[step])
            d = self.Flow[self.FlowSteps[step]]
            if d['default'] == "":
                print(d['executable'])
            else:
                print (d[d['default']]['executable'])
                print (d[d['default']]['arguments'])

        return
