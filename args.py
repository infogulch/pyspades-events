import inspect

def argspec_set(func):
    if not hasattr(func, 'argspec'):
        func.argspec = inspect.getargspec(func)

def argspec_iscompat(func, lenargs):
    spec = func.argspec
    minargs = len(spec.args) - len(spec.defaults or ())
    maxargs = len(spec.args) if spec.varargs is None else float("infinity")
    return minargs <= lenargs <= maxargs

class ArgCountError(Exception):
    pass
