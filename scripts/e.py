
def apply_script(events):
    def some_event(conn):
        print "Some event called, blocked!"
        return True
    
    events.subscribe(some_event, 'some_event', events.BLOCK)
