#!/usr/bin/env python2
# -*- coding:utf-8 -*-

__doc__ = '''
Learn refactoring step by step
python edition
'''
import unittest


class Movie(object):
    REGULAR = 0
    NEW_RELEASE = 1
    CHILDRENS = 2

    def __init__(self,title,price_code):
        self.title, self.price_code = title, price_code


class Rental(object):

    def __init__(self,movie,days_rented):
        self.movie, self.days_rented = movie, days_rented

    def charge(self):
        result = 0
        result = {
                Movie.REGULAR: lambda result: result + 2 + (self.days_rented - 2) * 1.5 if self.days_rented > 2 else result + 2,
                Movie.NEW_RELEASE: lambda result: result + self.days_rented * 3,
                Movie.CHILDRENS: lambda result: result + 1.5 + (self.days_rented - 3) * 1.5 if self.days_rented > 3 else result+ 1.5
            }[self.movie.price_code](result)
        return result


class Customer(object):

    def __init__(self,name):
        self.name = name
        self.rentals = []

    def add_rental(self,arg):
        self.rentals.append(arg)

    def statement(self):
        total_amount, frequent_renter_points = 0, 0
        result = 'Rental Record for %s\n' % self.name
        for element in self.rentals:
            this_amount = self.amount_for(element)

            # add frequent renter points
            frequent_renter_points += 1
            # add bonus for a two day new release rental
            if element.movie.price_code == Movie.NEW_RELEASE and element.days_rented > 1:
                frequent_renter_points += 1
            # show figures for this rental
            result += '\t' + element.movie.title + '\t' + str(this_amount) + '\n'
            total_amount += this_amount

        #add footer lines
        result += 'Amount owed is %s\n' % total_amount
        result += 'You earned %s frequent renter points' % frequent_renter_points

        return result

    def amount_for(self,rental):
        return rental.charge()


class VideoRentalTest(unittest.TestCase):
    def testMovies(self):
        customer = Customer('Chap')

        movie1 = Movie('Joe Versus the Volcano', Movie.REGULAR)
        rental1 = Rental(movie1, 5)
        customer.add_rental(rental1)
        statement1 = 'Rental Record for Chap\n\tJoe Versus the Volcano\t6.5\nAmount owed is 6.5\nYou earned 1 frequent renter points' 
        self.assertEqual(customer.statement(),statement1)

        movie2 = Movie('Sleepless in Seattle', Movie.CHILDRENS)
        rental2 = Rental(movie2, 1)
        customer.add_rental(rental2)
        statement2 = 'Rental Record for Chap\n\tJoe Versus the Volcano\t6.5\n\tSleepless in Seattle\t1.5\nAmount owed is 8.0\nYou earned 2 frequent renter points'
        self.assertEqual(customer.statement(),statement2)

        movie3 = Movie('You\'ve Got Mail', Movie.NEW_RELEASE)
        rental3 = Rental(movie3, 15)
        customer.add_rental(rental3)
        statement3 = "Rental Record for Chap\n\tJoe Versus the Volcano\t6.5\n\tSleepless in Seattle\t1.5\n\tYou've Got Mail\t45\nAmount owed is 53.0\nYou earned 4 frequent renter points"
        self.assertEqual(customer.statement(),statement3)


if __name__ == '__main__':
    unittest.main()
