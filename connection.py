
class Connection(object):
    def __init__(self, events):
        self.events = events
        #self.events.subscribe(Connection.some_event)
    
    def invoke(self, name, *args, **kwargs):
        "Easy invoke for connection-specific events."
        return self.events.invoke(name, *((self,)+args), **kwargs)
