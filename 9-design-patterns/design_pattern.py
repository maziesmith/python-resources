##################################################
#  Design Patterns with First Class Functions
##################################################
'''
Strategy Pattern
'''
# Define a family of algorithms, encapsulate each one, and make them interchangeable.
# Strategy lets the algorithm vary independently from clients that use it.
# Example Order uses Promotion and we can implement variations of Promotions objects

# Context
# Provides a service by delegating some computation to interchangeable components
# that implement alternative algorithms. In the ecommerce example, the context is
# an Order, which is configured to apply a promotional discount according to one of
# several algorithms.
# Strategy
# The interface common to the components that implement the different algorithms.
# In our example, this role is played by an abstract class called Promotion.
# Concrete Strategy
# One of the concrete subclasses of Strategy. FidelityPromo, BulkPromo, and Large
# OrderPromo are the three concrete strategies implemented.

from abs import ABC, abstractmethod
from collections import namedtuple

Customer = namedtuple('Customer','name fidelity')

class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product 
        self.quantity = quantity
        self.price = price 

    def total(self):
        return self.price * self.quantity 

class Order: # the Context
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer 
        self.cart = list(cart)
        self.promotion = promotion 
    
    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total 

    def due(self):
        if self.promotion is None:
            discount = 0 
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount 
    
    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())


class Promotion(ABC): # the Strategy: an abstract abse class 
    @abstractmethod
    def discount(self, order):
        """Return discount as a positive dollar amount"""

class FidelityPromo(Promotion): # a concrete strategy 
    """ discount for customer with fidelity points"""
    def discount(self, order):
        return order.total()*0.5 if order.customer.fidelity >=1000 else 0 
    
class BulkItemPromo(Promotion): # second concrete strategy 
    """discounts for each lineitem with 20 more units"""
    def discount(self, order):
        discount = 0
        for item in order.cart:
            if item.quantity >=20:
                discount+=item.total()*0.1
        return discount 

# joe = Customer('John Doe', 0)
# cart = [LineItem('banana', 4, .5),
#         LineItem('apple', 10, 1.5),
#         LineItem('watermellon', 5, 5.0)]
# Order(joe, cart, FidelityPromo())


# Refactoring Using functions as objects 
# replace concrete strategies with simple functions 
from collections import namedtuple 
Customer = namedtuple('Customer', 'name fidelity')

class LineItem:
    def __init__(self, prodcut, quantity, price):
        self.product = prodcut
        self.quantity = quantity
        self.price = price 
    
    def total(self):
        return self.price * self.quantity 
    
class Order: # the Context 
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer 
        self.cart = list(cart)
        self.promotion = promotion 
    
    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total 

    def due(self):
        if self.promotion is None:
            discount = 0 
        else:
            discount = self.promotion(self) # using the function. To compute a discount, just call the self.promotion() function.
        return self.total() - discount 

def fidelity_promo(order):
    """5% discount for customers with 1000 or more fidelity points"""
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0

# To apply a discount strategy to an Order, just pass the promotion function as an
# argument.
Order(joe, cart, fidelity_promo)

# Find the best promos 
promos = [fidelity_promo, bulk_item_promo, large_order_promo]

def best_promo(order):
    """Select best discount available
    """
    return max(promo(order) for promo in promos)

# Alternative using module
promos = [globals()[name] for name in globals()
            if name.endswith('_promo')
            and name != 'best_promo']
    
# globals()
# Return a dictionary representing the current global symbol table. This is always the
# dictionary of the current module (inside a function or method, this is the module
# where it is defined, not the module from which it is called).


'''
Command 
'''

# The goal of Command is to decouple an object that invokes an operation (the Invoker)
# from the provider object that implements it (the Receiver). In the example from Design
# Patterns, each invoker is a menu item in a graphical application, and the receivers are
# the document being edited or the application itself.

# Building a list from the commands arguments ensures that it is iterable and keeps
# a local copy of the command references in each MacroCommand instance.
# When an instance of MacroCommand is invoked, each command in self.com
# mands is called in sequence.

class MacroCommand:
    """A command that executes a list of commands"""
    def __init__(self, commands):
        self.commands = list(commands)
    
    def __call__(self):
        for command in self.commands:
            command()


