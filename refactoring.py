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
        self.title = title
        self.set_price_code(price_code)

    def set_price_code(self, value):
        self.price_code = value
        if self.price_code == Movie.REGULAR:
            self.price = RegularPrice()
        elif self.price_code == Movie.NEW_RELEASE:
            self.price = NewReleasePrice()
        elif self.price_code == Movie.CHILDRENS:
            self.price = ChildrensPrice()

    def charge(self, days_rented):
        result = self.price.charge(days_rented)
        return result

    def frequent_renter_points(self, days_rented):
        return self.price.frequent_renter_points(days_rented)


class DefaultPrice(object):
    def frequent_renter_points(self, days_rented):
        return 1


class RegularPrice(DefaultPrice):
    def charge(self, days_rented):
        result = 2
        if days_rented > 2:
            result += (days_rented - 2) * 1.5
        return result


class NewReleasePrice(DefaultPrice):
    def charge(self, days_rented):
        result = days_rented * 3
        return result

    def frequent_renter_points(self, days_rented):
        return 2 if days_rented > 1 else 1


class ChildrensPrice(DefaultPrice):
    def charge(self, days_rented):
        result = 1.5
        if days_rented > 3:
            result += (days_rented - 3) * 1.5
        return result


class Rental(object):

    def __init__(self,movie,days_rented):
        self.movie, self.days_rented = movie, days_rented

    def charge(self):
        return self.movie.charge(self.days_rented)

    def frequent_renter_points(self):
        return self.movie.frequent_renter_points(self.days_rented)


class Customer(object):

    def __init__(self,name):
        self.name = name
        self.rentals = []

    def add_rental(self,arg):
        self.rentals.append(arg)

    def statement(self):
        frequent_renter_points = 0
        result = 'Rental Record for %s\n' % self.name
        for element in self.rentals:
            this_amount = element.charge()

            frequent_renter_points += element.frequent_renter_points()

            # show figures for this rental
            result += '\t' + element.movie.title + '\t' + str(element.charge()) + '\n'

        #add footer lines
        result += 'Amount owed is %s\n' % self.total_charge()
        result += 'You earned %s frequent renter points' % self.total_frequent_renter_points()

        return result

    def total_charge(self):
        result = 0
        for element in self.rentals:
            result += element.charge()
        return result

    def total_frequent_renter_points(self):
        return sum([rental.frequent_renter_points() for rental in self.rentals])


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
