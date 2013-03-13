
def apply_script(events):
    # subscribe to an event. use a custom function name, 
    # and specify the event name manually
    @events.subscribe('some_event')
    def myhandler(conn):
        print 'some_event handler in %s' % __name__
