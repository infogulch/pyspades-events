
# 3 p's, typo!
def appply_script(events):
    @events.subscribe
    def some_event(conn):
        print 'some_event handler in %s' % __name__
