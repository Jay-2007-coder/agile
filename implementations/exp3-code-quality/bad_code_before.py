"""
book_store.py - Online Book Store with intentional code quality issues
for demonstrating Pylint/Flake8 analysis.

Experiment 3: Code Quality Analysis
"""

# BAD CODE (before quality fixes) - this is intentional for demo purposes
import os,sys   # E401: multiple imports on one line
import math  
import random

# Unused import (will be flagged)

class book:  # C0115: Missing class docstring; C0103: wrong naming convention
    def __init__(self,id,title,author,price,stock):  # Bad spacing
        self.id=id  # E225: missing whitespace
        self.title=title
        self.author=author
        self.price=price
        self.stock=stock
    
    def get_info( self ):  # E203: whitespace before ':'
        print( "ID: "+str(self.id)+", Title: "+self.title )  # W1514

class BookStore:
    """Online Book Store management system."""
    
    def __init__(self):
        self.books=[]   # E225
        self.Users = {}  # Inconsistent naming
    
    def addbook(self,book):  # C0103: should be add_book
        """Add a book to the store."""
        if book!=None:  # E711: comparison to None
            self.books.append(book)
            return True
        else:
            return False
    
    def search(self,keyword):
        """Search books by keyword."""
        results = []
        for b in self.books:
            if keyword in b.title:
                results.append( b )  # E203
        return results
    
    def get_total(self):
        x=0  # C0103: bad variable name
        for b in self.books:
            x=x+b.price  # E225
        return x

    def unused_method(self):  # W0612: unused variable inside
        unused_var = "I am never used"  # noqa
        pass

# Long line example (PEP8 violation - should be < 79 chars)
def calculate_discount(price, discount_percent, tax_rate, minimum_order_value, is_premium_member, has_coupon):
    """Calculate final price with discount."""
    if is_premium_member == True:  # E712: comparison to True
        discount_percent = discount_percent + 5
    
    discount_amount = price * (discount_percent / 100)
    discounted_price = price - discount_amount
    
    if has_coupon == True:
        discounted_price = discounted_price * 0.9
    
    final_price = discounted_price * (1 + tax_rate / 100)
    return final_price


def bad_password_check(password):
    """Check password - security issue (for Bandit demo)."""
    # B105: hardcoded password
    if password == "admin123":
        return True
    return False


# Magic numbers (W0141)
def get_price_category(price):
    if price < 200:   # Magic number
        return "cheap"
    elif price < 500:  # Magic number  
        return "medium"
    else:
        return "expensive"
