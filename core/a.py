# core script

def apply_script(events):
    def scripts_loaded():
        print 'Core script %s in scripts_loaded event' % __name__
    
    events.subscribe(scripts_loaded)
