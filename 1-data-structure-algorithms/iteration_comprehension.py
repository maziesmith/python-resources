
##################################################
# Loops 
##################################################
# for loop
for name in ['a','b','c']:
    print(name)

# accumulator pattern
nums = [1,2,3,4]
res = 0
for w in nums:
    res = res + w 
print(res)

# traversal
for counter, item in enumerate(['a','b','c']):
    print(counter, item)

for n in range(len(fruit)):
    print(n, fruit[n])

# enumeration
# return an iterable. using for loop then index, value
fruits = ['apple', 'pear', 'apricot', 'cherry', 'peach']
for idx, fruit in enumerate(fruits):
    print(idx, fruit)

for i, item in enumerate(my_items):
    print(f'{i}:{item}')



# while loop
def sumTo(aBound):
    """ Return the sum of 1+2+3 ... n """
    theSum  = 0
    aNumber = 1
    while aNumber <= aBound:
        theSum = theSum + aNumber
        aNumber = aNumber + 1
    return theSum

# break and continue
while True:
    print("this phrase will always print")
    break
    print("Does this phrase print?")

print("We are done with the while loop.")

# continue is the other keyword that can control the flow of iteration. Using continue allows the program to immediately “continue” with the next iteration. 
# The program will skip the rest of the iteration, recheck the condition, and maybe does another iteration depending on the condition set for the while loop.

for name in student_names:
    if name == "mark":
        print('found him'+name)
        break
    print("currently testing "+name)

for name in student_names:
    if name == "bort":
        continue # continue to the next iteration
        print("found him"+name)
    print("currently testing"+name)


# two approach to break out of the loop if found item
#  - return early 
def coprime(a, b):
    for i in range(2, min(a,b)+1):
        if a % i == 0 and  b % i == 0:
            return False 
    return True 

#  - have a result variable indicating if found and break out of the loop if found
def coprime2(a, b):
    is_coprime = True
    for i in range(2, min(a,b)+1):
        if a % i == 0 and b % i == 0:
            is_coprime = False 
            break 
    return is_coprime 


##################################################
# Iteration
##################################################


# using iterator by next
with open('/etc/passwd') as f:
    while True:
        line = next(f, None)
        if line is None:
            break
        print(line, end='')


'''
delegating iterator to __iter__()
'''
class Node:
    def __init__(self, value):
        self._value = value 
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)
    
    def add_child(self, node):
        self._children.append(node)
    
    def __iter__(self):
        return iter(self._children)

# example 
if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    for ch in root:
        print(ch)

# Python’s iterator protocol requires __iter__() to return a special iterator object that
# implements a __next__() method to carry out the actual iteration.


##################################################
# List Comprehensions & Maps
##################################################
'''
Comprehensions
'''
l = [i*2 for i in range(10)]
d = {i: i*2 for i in range(10)}

# multi-input comprehensions

# nested comprehensions
vals = [[y*3 for y in range(x)] for x in range(10)]

even_squares = [x * x for x in range(10)
                if x % 2 == 0] 

values = [expression 
          for item in collection 
          if condition]


# list comprehensions do everything map and filter functions do 
symbols = '$¢£¥€¤'

beyond_ascii = [ord(s) for s in symbols if ord(s) > 127]

beyond_ascii = list(filter(lambda c: c > 127, map(ord, symbols)))


'''
Cartesian Product 
'''

[(x,y) for x in range(5) for y in range(3)]

tshirts = [(color, size) for color in colors for size in sizes]


'''
multiple levels
'''
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]
print(flat)
# >>> [1, 2, 3, 4, 5, 6, 7, 8, 9]

# if you want to square the value in each cell of a two-dimensional matrix.
squared = [[x**2 for x in row] for row in matrix]
print(squared)
# >>> [[1, 4, 9], [16, 25, 36], [49, 64, 81]]

[(x, y) for x in range(10) for y in range(x)]
# same thing as before
result = []
for x in range(10):
    for y in range(x):
        result.append((x, y))


'''
Generator Expressions
'''

# To initialize tuples, arrays, and other types of sequences, you could also start from a
# listcomp, but a genexp saves memory because it yields items one by one using the iterator
# protocol instead of building a whole list just to feed another constructor.

# When processing one item at a time, we only need the current object stored in memory at any one moment. But when we create a container, all the
# objects have to be stored in that container before we start processing them.

# Genexps use the same syntax as listcomps, but are enclosed in parentheses rather than
# brackets.

tuple(ord(symbol) for symbol in symbols)


# cartesian product in a generator expression
colors = ['black', 'white']
sizes = ['S','M','L']
# using a generator expression saves the expense of building a list of a lot of items
# generator expressions
for tshirt in ('%s %s' % (c, s) for c in colors for s in sizes):
    print(tshirt)


'''
map()
'''
# map - apply a function to every element in a sequence, producing a new sequence
# returns a map object, it only produces values as it's needed 
map(ord, 'the quick brown') # ord is the mapping function
list(map(ord, 'the quick brown')) # use list for use a for loop 

# multiple input sequences 
# map can accept any number of input sequences 
map(func, a, b, c) 
def combine(size, color, animal):
    return '{} {} {}'.format(size, color, animal)
list(map(combine, sizes, colors, animals))

# filter
# apply a function to each element in a sequence, constructing a new sequence with the elements for which the function returns True
# returns lazy iterable, needs to apply list to evaluate
filter(is_odd, [1,2,3,4,5])
positives = filter(lambda x:x>0, [1,-5,0,2])

# reduce 
# apply a function to the elements of a sequence, reducing them to a single value 
from functools import reduce
import operator
reduce(operator.add, [1,2,3])

# multiply function to print out intermediate results
def mul(x, y):
    print('mul {} {}'.format(x, y))
    return x*y
reduce(mul, range(1,10))

# map and filter functions 
list(map(factorial, range(6)))
[factorial(n) for n in range(6)]

list(map(factorial, filter(lambda n: n%2, range(6))))
[factorial(n) for n in range(6) if n%2]

# reduce 
# repeatedly apply a function to the elements of a sequence, reducing them to a single value 
from functools import reduce 
import operator 
reduce(operator.add, [1,2,3,4,5])
# takes an optional default value 
values = [1,2,3]
reduce(operator.add, values, 0)
 

##################################################
# Iterators and Generators
##################################################

'''
Iterators and Generators
'''

# iterable - an object which implements the __iter__() method (which returns an iterator)
# an iterator is an object with a next() method and a done() method 
# all iterators are iterables which generally just return themselves with __iter__()
# generator creates iterator using functions

# iter() create an iterator
# next() get next element in sequence
# stopIteration signal the end of the sequence

def my_range(x):
    i =0
    while i <x:
        yield i
        i+=1
    
for n in my_range(4):
    print(n)

sq_list = [x**2 for x in range(10)]  # this produces a list of squares

sq_iterator = (x**2 for x in range(10))  # this produces an iterator of squares

iterable = ['a','b','c']
iterator = iter(iterable)
next(iterator) # prints 'a'
next(iterator) # prints 'b'

# for loop is a syntactic implementation for a while loop 
for item in iterable: 
    print(item)

# similar to 
iterator = iterable.__iter__()

while True: 
    item = iterator.__next__()
    print(item)


'''
Iterable vs.Iterator
'''

# python obtain iterators from iterables 

# iterables have an __iter__ method that instantiates a new iterator every time.
# Iterators implement a __next__ method that returns individual items, and an __iter__
# method that returns self.

s = 'ABC' # str 'ABC' is the iterable here
for char in s: # iterator behind the scenes
    print(char)

s = 'ABC'
it = iter(s) # build an iterator it from the iterable
while True: 
    try:
        print(next(it)) # call next on the iterator to obtain the next item 
    except StopIteration:
        del it
        break 

# classic iterator 
# iterator pattern
import re 
import reprlib 

RE_WORD = re.compile('\w+')
class Sentence: 
    def __init__(self, text):
        self.text = text
        self.words = RE_WORLD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)    
    
    # Sentence is iterable because it implements the __iter__ special method
    # which builds and returns a SentenceIterator
    def __iter__(self):
        return SentenceIterator(self.words)

class SentenceIterator:
    def __init__(self, words):
        self.words = words # holds a reference to the list of words
        self.index = 0 
    
    def __next__(self): 
        try:
            word = self.words[self.index]
        except IndexError: # if no word at self.index, raise StopIteration
            raise StopIteration()
        self.index+=1
        return word 
    
    def __iter__(self): #implement the self.__iter__
        return self 


# alternative implementation
# use the yield (generator function) to replace the SentenceIterator class 
import re 
import reprlib 

RE_WORD = re.compile('\w+')


class Sentence: 
    def __init__(self, text):
        self.text = text 
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)
    
    def __iter__(self):
        for word in self.words: 
            yield word 
        return 


# another example 
# loop through each of the words in a string and output them with the first letter capitalized 
class CapitalIterable:
    def __init__(self, string):
        self.string = string 

    def __iter__(self):
        return CapitalIterator(self.string)
    
    
class CapitalIterator:
    def __init__(self, string):
        self.words = [w.capitalize() for w in string.split()]
        self.index = 0 
    
    def __next__(self):
        if self.index = len(self.words):
            raise StopIteration()
    
        word = self.words[self.index]
        self.index += 1
        return word 
    
    def __iter__(self):
        return self 

# example utilizing the iterable 
iterable = CapitalIterable('the quick brown fox')
iterator = iter(iterable)
while True:
    try:
        print(next(iterator))
    except StopIteration:
        break 


# stateful iterator functions

def distinct(iterable):
    """return unique item by eliminating duplicates
    """
    seen = set()
    for item in iterable:
        if item in seen:
            continue
        yield item
        seen.add(item)

def run_distinct():
    items = [1,2,3,4]
    for item in distinct(items):
        print(item)

'''
__getitem__()
'''
# alternative, __getitem__ which works for consecutive integers

class AlternateIterable:
    def __init__(self):
        self.data=[1,2,3]
    def __getitem__(self, idx):
        return self.data[idx]

# extended iter()
iter(callable, sentinel) #callable that takes zero arguments, sentinel - iteration stops when callable produces this value

import random
class Sensor:
    def __iter__(self):
        return self
    def __next__(self):
        return random.random()

sensor = Sensor()
timestamps = iter(datetime.datetime.now, None)

'''
iterating in reverse 
'''

a = [1,2,3,4]
for x in reversed(a):
    print(x)

# print a file backwards 
f = open('somefile')
for line in reversed(list(f)):
    print(line, end='')

# reversed iteration can be customozed on user defined classes with the __reversed__() method
class Countdown:
    def __init__(self, start):
        self.start = start 
    
    # forward iterator 
    def __iter__(self):
        n = self.start 
        while n > 0:
            yield n 
            n -= 1

    # reverse iterator 
    def __reversed__(self):
        n = 1
        while n <= self.start:
            yield n 
            n += 1

'''
Stacking Iterators 
'''
# stacking generators together 
# yield acts as a kind of producer while for loop acts as a data consumer 
import os 
import fnmatch 
import gzip
import bz2
import re 

def gen_find(filepat, top):
    '''
    Find all filenames in a directory tree
    '''
    for path, dirlist, filelist is os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)

def gen_opener(filenames):
    '''
    Open a sequence of filenames one at a time 
    '''
    for filename in filenames:
        if filename.endswith('.gz'):
            f = gzip.open(filename, 'rt')
        elif filename.endswith('.bz2'):
            f = bz2.open(filename, 'rt')
        else:
            f = open(filename, 'rt')
        yield f 
        f.close()

def gen_concatenate(iterators):
    '''
    Chain a sequence of iterators together
    '''
    for it in iterators:
        yield from it 

def gen_grep(pattern, lines):
    '''
    Look for a regex pattern in a sequence of lines 
    '''
    pat = re.compile(pattern)
    for line in lines: 
        if pat.search(line):
            yield line 

lognames = gen_find('access-log*', 'www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?i)python', lines)
for line in pylines:
    print(line)



''' 
yield 
'''

# best practice use yield results instead of append to list 

def index_word_iter(text):
    if text:
        yield 0 
    for index, letter in enumerate(text):
        if letter == '':
            yield index+1 
# the iterator returned by the call can be converted to list 
result = list(index_word_iter(text_data))

# bad implementation using list 
def index_words(text):
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ‘ ‘:
            result.append(index + 1)
    return result


# the presence of the yield statement turns a function into a generator 
# customize an iteration pattern 
def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x 
        x += increment 

# yield from 
from collections import Iterable 

def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)
        else:
            yield x 

items = [1, 2, [3, 4, [5, 6], 7], 8]
for x in flatten(items):
    print(x)

# yield from flatten(x) is the same as for i in flatten(x): yield i 
n 


# using yield as generator expressions
import sys
inname, outname = sys.argv[1:3]

# filter for specific patterns
def warnings_filter(insequence):
    for l in insequence:
        if 'WARNING' in l:
            yield l.replace('\tWARNING', '')

with open(inname) as infile:
    with open(outname, "w") as outfile:
        filter = warnings_filter(infile)
        for l in filter:
            outfile.write(l)


'''
slice of an iterator 
'''
# use the itertools.isslice() function for taking slices of iterators and generators 

def count(n):
    while True: 
        yield n 
        n += 1

c = count(0)
import itertools 
for x in itertools.islice(c, 10, 20):
    print(x)

# want everything beyond the first three items 
# for x in itertools.islice(c, 3, None):



