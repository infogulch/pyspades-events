import sys

from events import Events
from connection import Connection

events = Events()
connection = Connection(events)
script_recorders = {}

def load_script(name):
    fullname = "scripts.%s" % name
    try:
        module = __import__(fullname, globals(), locals(), [fullname])
        recorder = events.recorder()
        module.apply_script(recorder)
        script_recorders[name] = recorder
    except ImportError as e:
        print "(script '%s' not loaded: %r)" % (name, e)
    except (AttributeError, TypeError) as e:
        print "(script '%s' not loaded: %r)" % (name, e)
        sys.modules.pop(fullname, None)
        sys.modules.pop('scripts', None)

def unload_script(name):
    if name in script_recorders:
        events.invoke('unload_script_%s' % name)
        fullname = "scripts.%s" % name
        script_recorders[name].unsubscribe_all()
        script_recorders.pop(name, None)
        sys.modules.pop(fullname, None)
        sys.modules.pop('scripts', None)
    else:
        print "Error, script not loaded"

events.subscribe(load_script)
events.subscribe(unload_script)

# load scripts
script_names = ["a","b","c","d","e"]
for name in script_names:
    events.invoke('load_script', name)

events.invoke('scripts_loaded')

# invoke an event
events.invoke('some_event', connection)

print "unload script a"
events.invoke('unload_script', 'a')

# invoke the event again
connection.invoke('some_event')

print "load script a"
events.invoke('load_script', 'a')

# invoke the event again
connection.invoke('some_event')
