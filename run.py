import sys
import os

from events import Events
from connection import Connection

events = Events()
connection = Connection(events)
script_recorders = {}

def _pop_modules(parts):
    while parts:
        sys.modules.pop(".".join(parts), None)
        parts = parts[:-1]

def load_script(name, module = "scripts"):
    parts = module, name
    error = None
    try:
        if parts in script_recorders:
            raise ImportError("Script already loaded")
        module = __import__(".".join(parts), globals(), locals(), ["script"])
        recorder = events.recorder()
        module.apply_script(recorder)
    except ImportError as e:
        error = "Script '%s' not loaded: %r" % (".".join(parts), e)
    except (AttributeError, TypeError, Exception) as e:
        error = "Script '%s' not loaded: %r" % (".".join(parts), e)
        _pop_modules(parts)
    else:
        script_recorders[parts] = recorder
    if error:
        print error
        return error

def unload_script(name, module = "scripts"):
    parts = module, name
    if parts in script_recorders:
        script_recorders[parts].unsubscribe_all()
        script_recorders.pop(parts, None)
        _pop_modules(parts)
    else:
        error = "Script '%s' not unloaded: it doesn't exist" % (name)
        print error
        return error

events.subscribe(load_script)
events.subscribe(unload_script)

# load all core scripts
for fname in os.listdir("./core"):
    if fname.endswith(".py") and fname != '__init__.py':
        events.invoke('load_script', fname[:-3], "core")

# load selected user scripts
script_names = ["a","b","c","d","f"]
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

print "load script e"

# load blocker script
events.invoke('load_script', 'e')

events.invoke('some_event', connection)

print "unload script e"

events.invoke('unload_script', 'e')

connection.invoke('some_event')
