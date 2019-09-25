##################################################
#  Functions Basics
##################################################

'''
Function as Object
'''

# functions are first class objects, i.e.
#  - created at runtime
#  - assigned to a variable or element in a data structure
#  - passed as an argument to a function
#  - returned as the result of a function 

# Create and test a function, then read its __doc__ and check its type
def factorial(n):
    '''returns n!'''
    return 1 if n < 2 else n * factorial(n-1)
# >>> factorial(42)
# 1405006117752879898543142606244511569936384000000000
# doc is one of several attributes of function objects 
# >>> factorial.__doc__ 
# 'returns n!'
# factorial is an instance of the function class 
# >>> type(factorial)
# <class 'function'>


'''
Variables and Parameters 
''' 
# variables and parameters are local 

# default value
# default value is determined at the time that the function is defined, not at the time that it is invoked. 
initial = 7
def f(x, y =3, z=initial):
    print("x, y, z, are: " + str(x) + ", " + str(y) + ", " + str(z))


# deep and shallow copies
# When you copy a nested list, you do not also get copies of the internal lists. 
# This means that if you perform a mutation operation on one of the original sublists, the copied version will also change.



##################################################
# Callable Objects 
##################################################


# The call operator (i.e., ()) may be applied to other objects beyond user-defined functions.
# To determine whether an object is callable, use the callable() built-in function.
# callable instances

# following callable types 
#  - user defined functions, def and lambda 
#  - built in functions
#  - built in methods 
#  - methods, functions define in the body of a class 
#  - classes: when invoked, class runs its __new__ method to create an isntance, then __init__ to initialize it 
#  - class instances: if a class defines a __call__ method then instances can be invoked as functions
#  - generator functions: functions or methods that use the yield keyword. When called, generator functions return a generator object

__call__() # call method

# calling a class invokes the constructor





##################################################
# High-Order Functions
##################################################

# A function that takes a function as argument or returns a function as the result is a
# higher-order function.

# example: map, filter, reduce, apply
# example: sorted function which take an optional key argument 
sorted(fruits, key=len)
# any one-argument function can be used with a key 
def reverse(word):
    return word[::-1]
sorted(fruits, key=reverse)






##################################################
# Lambda Functions
##################################################

# lambda functions
# same as anonymous functions
sorted(scientists, key=lambda name: name,split()[-1]) # creating a callable function using lambda

# using callable() to detect callable 
def is_event(x):
    return x % 2 == 0
callable(is_event)

##################################################
# Extended Arguments 
##################################################

# extended arguments syntax

def hypervolume(length, *lengths): # accept a number of arguments with a lower bound
    v = length
    for item in lengths:
        v*=length
    return v

# keyword arguments
def function_name(arg1, arg2=8) # arg1 is positional argument, and arg2 is keyword argument, and 8 is default value

def extended(*args, **kwargs): # args is passed as a tuple

# forwarding arguments
# pull args into another function
def trace(f, *args, **kwargs)


# local functions
# functions defined within the scope of other functions
def sort_by_last_letter(strings):
    def last_letter(s): # function is created each time def is called
        return s[-1]
    return sorted(strings, key=last_letter)

# uselful for specialized, one-off functions
# aid in code organization and readability
# similar to lambdas but more general

# functions can be treated like any other oject
# closures - maintain references to objects from earlier scopes 

# function factories - functions that return new, specialized functions
def raise_to(exp):
    def raise_to_exp(x):
        return pow(x, exp)
    return raise_to_exp

# LEGB
# global keyword - introduces names from the enclosing namespace into the local namespace 
# nonlocal - introduce names from enclosing namespace into the local namespace

##################################################
# Decorators
##################################################

# decorators
# modify or enhance functions without changing their definition
# implemented as callables that take and return other callables 
@my_decorator 
def my_function(x,y): # function object
    return x+y

# example of defining a decorator which puts things as unicode
# takes function f and returns wrap, which is a similar function to f 
def escape_unicode(f):
    def wrap(*args, **kwargs):
        x = f(*args, **kwargs)
        return ascii(x)
    return wrap

@escape_unicode
def northern_city():
    return 'Tromse'

# other objects (callables) can be decorators as well 
# classes as decorators
# example, class CallCount which counts how many times function is called
class CallCount:
    def __init__(self, f): # init new instance
        self.f = f
        self.count = 0 
    
    def __call__(self, *args, **kwargs): # makes it a callable wrap function 
        self.count +=1
        return self.f(*args, **kwargs)

@CallCount
def hello(name):
    print('Hello, {}'.format(name))


# instances as decorators


# multiple decorators
@decorator1
@decorator2
def some_func():
# first passed to decorator2 then passed to decorator1

# naive decorators can lose important metadata
# help() only shows the wrapper function not the original function
# so have to update the __name__ and __doc__ 
def noop(f):
    @functiontools.wrap(f)
    def noop_wrapper():
        return f()
    noop_wrapper.__name__ = f.__name__
    noop_wrapper.__doc__ = f.__doc__
    return noop_wrapper

# example check non negatives of argments 
def check_non_negative(index):
    # below is a decorator function 
    def validator(f):
        def wrap(*args):
            if args[index]<0:
                raise ValueError('Argument {} must be non-negative.'.format(index))
            return f(*args)
        return wrap
    return validator

@check_non_negative(1)
def create_list(value, size):
    return [value] *size 



##################################################
# Function Introspection
##################################################

# Like the instances of a plain user-defined class, a function uses the __dict__ attribute
# to store user attributes assigned to it

# Within a function object, the __defaults__ attribute holds a tuple with the default
# values of positional and keyword arguments. The defaults for keyword-only arguments
# appear in __kwdefaults__. The names of the arguments, however, are found within the
# __code__ attribute, which is a reference to a code object with many attributes of its own.


##################################################
# Functional Programming
##################################################
# the operator module 
# provide arithmetic operator as a function 
from functools import reduce 
from operator import mul 

def fact(n):
    return reduce(mul, range(1, n+1))
    # same as 
    # return reduce(lambda a, b: a*b, range(1, n+1))

#  using itemgetter and attrgetter to build custom functions
metro_data = [
    ('Tokyo', 'JP', 36.933, (35.682, 130.212)),
    ('Mexico City', 'MX', 20.142, (19.682, -30.212))
]

from operator import itemgetter
for city in sorted(metro_data, key=itemgetter(1)):
    print(city)
# same as 
# for city in sorted(metro_data, key=lambda fields: fields[1])

# A sibling of itemgetter is attrgetter, which creates functions to extract object attributes
# by name. If you pass attrgetter several attribute names as arguments, it also
# returns a tuple of values. In addition, if any argument name contains a . (dot), attrget
# ter navigates through nested objects to retrieve the attribute.



