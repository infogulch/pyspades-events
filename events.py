EVENT_LEVELS = BLOCK, CONSUME, NOTIFY = range(3)

# events:          dict of (event_name:handler_levels)
# handler_levels:  3-tuple of sets of functions

class Events(object):
    def __init__(self, default = NOTIFY):
        self.default = default
        self.events = {}
    
    @property
    def default(self):
        return self._default[0] if hasattr(self, "_default") else NOTIFY
    
    @default.setter
    def default(self, value):
        if not hasattr(self, "_default"):
            self._default = [NOTIFY]
        if value in EVENT_LEVELS:
            self._default[0] = value
    
    def _subscribe(self, func, name, level):
        self.events[name][level].add(func)
    
    # def subscribe(self, func, name = None, level = None):
    def subscribe(self, *args):
        args = list(args)
        func = args.pop(0) if len(args) and hasattr(args[0], "__call__") else None
        cname = args.pop(0) if len(args) else None
        level = args.pop(0) if len(args) and args[0] in EVENT_LEVELS else self.default
        def sub(func):
            name = (cname or func.__name__).lower()
            if not self.events.has_key(name):
                self.events.setdefault(name, (set(), set(), set()))
            self._subscribe(func, name, level)
            return func
        return sub(func) if func else sub
    
    def _unsubscribe(self, func, name, level):
        self.events[name][level].discard(func)
        if not any(self.events[name]):
            self.events.pop(name)
    
    def unsubscribe(self, func, name = None, level = None):
        name = name.lower()
        if level not in EVENT_LEVELS:
            level = self.default
        if self.events.has_key(name):
            self._unsubscribe(func, name, level)
    
    def invoke(self, name, *args, **kwargs):
        max_level = kwargs.get('max_level', NOTIFY)
        if not self.events.has_key(name):
            return None
        event = self.events[name]
        for level in EVENT_LEVELS:
            if level > max_level:
                break
            for func in event[level]:
                # todo: wrap in try block
                result = func(*args)
                if level < NOTIFY and result:
                    return result
        return None
    
    def recorder(self):
        class Recorder(Events):
            def __init__(self, existing):
                # all properties are objects, so when they are copied
                # only references are made; so changes to one apply to all
                self.events = existing.events
                self._default = existing._default
                self.recorded = set()
            
            def _subscribe(self, func, name, level):
                Events._subscribe(self, func, name, level)
                self.recorded.add((func, name, level))
            
            def _unsubscribe(self, func, name, level):
                Events._unsubscribe(self, func, name, level)
                self.recorded.discard((func, name, level))
            
            def unsubscribe_all(self):
                for args in self.recorded.copy():
                    self._unsubscribe(*args)
        
        return Recorder(self)