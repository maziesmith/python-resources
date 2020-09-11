##################################################
# Context Manager
##################################################
# an object designed to be used in a with statement
# a context-manager ensures the resources are properly and automatically managed

with context-manager:
    # enter and exit are always called no matter how the body block terminates
    enter() # prepares the context manager
    body 
    exit() # clean up 

# a context manager ensures that resources are properly and automatically managed
with open('important_data.txt', 'w') as f:
    f.write('The secret password is 12345')

# files are context managers
# file's exit() code closes the file 


'''
context manager protocol
'''
__enter__(self)
# if __enter__ throws an exception, then never execute the following
# expression.__enter__() is bound to the as variable
# common for __enter__ to return itself
# for example, file.__enter__() returns the file object itself 

# __exit__ can do different things depending on how the with block terminates
# called when with-statement block exits
# exception type, exception object, exception traceback
__exit__(self, exc_type, exc_val, exc_tb)
# __exit__() called when with statement body exits
# __exit__() can check type for None to see if an exception was thrown 

# by default, __exit__() propagates exceptions thrown from the with-block
# if __exit__() returns False, the exception is propagated (with statement asks if need to swallow the exception, if false, reraises the exception)

# naive implementation of a context manager 
class LoggingContextManager:
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None: 
            print('normal exit detected')
        else:
            print('exception detected - type={}, value={}, traceback={}').format(
                exc_type, exc_val, exc_tb)) 


with LoggingContextManager() as x:
    print(x)


class ManagedFile:
    def __init__(self, name):
        self.name = name 

    def __enter__(self):
        self.file = open(self.name, 'w')
        return self.file 

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file: 
            self.file.close()

with ManagedFile('hello.txt') as f: 
    f.write('Hello world')


'''
contextlib
'''
# standard library module for working with context managers
# provides additional tools that help turn functions into context maangers

# enforce the call of an object's close() method 

from contextlib import closing 
with closing(open("outfile.txt", "w")) as output:
    output.write("abc")

# because __enter__() and __exit__() are defined for the object that handles file I/O we can use the with directly
with open("outfile.txt", "w") as output: 
    pass 

# contextlib.contextmanager is a decorator you can use to create new context managers
# Essentially the contextlib.contextmanager decorator wraps the function in a class that implements the __enter__ and __exit__ methods

# find the yield keyword: everything before it deals with setting up the context, which entails creating
# a backup file, then opening and yielding references to the readable and writable file
# handles that will be returned by the __enter__ call. The __exit__ processing after the
# yield closes the file handles and restores the file from the backup if something went wrong.

@contextlib.contextmanager
def my_context_manager():
    # Enter
    try: # like __enter__()
        yield [value] # like __enter__()'s return statement
        # normal exit
    except:
        # exceptional exit from with block
        raise
with my_context_manager() as x:

# exception propagated from inner context mansgers will be seen by outer context managers

# passing multiple context managers
with nest_test('a'), nest_test('b'):
    pass

# example
@contextmanager
def session_scope(commit=True):
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        if commit:
            session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


from contextlib import contextmanager

@contextmanager
def managed_resource(*args, **kwds):
    # Code to acquire resource, e.g.:
    resource = acquire_resource(*args, **kwds)
    try:
        yield resource
    finally:
        # Code to release resource, e.g.:
        release_resource(resource)

with managed_resource(timeout=3600) as resource:
# Resource is released at the end of this block,
# even if code in the block raises an exception

# In this case, managed_file() is a generator that first acquires the
# resource. After that, it temporarily suspends its own execution and
# yields the resource so it can be used by the caller. When the caller
# leaves the with context, the generator continues to execute so that any
# remaining clean-up steps can occur and the resource can get released
# back to the system.


@contextlib.contextmanager 
def managed_file(name):
    try:
        f = open(name, 'w')
        yield f 
    finally:
        f.close()

with managed_file('hello.txt') as f:
    f.write('hello world')





