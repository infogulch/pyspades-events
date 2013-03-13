
def apply_script(events):
    # subscribe to an event. use the function name as the name of the event
    def some_event(conn):
        print 'some_event handler in %s' % __name__
    events.subscribe(some_event)
    
