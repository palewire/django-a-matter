# -*- coding: utf-8 -*-
from django.test import TestCase

from a_matter.models import *
from places.models import *

from django.contrib.gis.geos import Point

# Helper base class for changes tests that need data.
class AMatterTestCase(TestCase):
    
    def createReporters(self):
        # Ruben Salazar
        ciudad_juarez = Place.objects.create(
            name = 'Ciudad Juarez',
            slug = 'ciudad-juarez',
            description = 'A city in Chihuahua, Mexico',
            point = Point(31.63722222, -106.42861111)
        )
        los_angeles = Place.objects.create(
            name = 'Los Angeles',
            slug = 'los-angeles',
            description = 'A city in California, USA.',
            point = Point(34, -118.3)
        )
        chicago = Place.objects.create(
            name = 'Chicago',
            slug = 'chicago',
            description = 'A city in Illinois, USA.',
            point = Point(41.85, -87.65)
        )
        journalist = PersonType.objects.create(
            name = 'Journalist',
            slug = 'journalist',
        )
        tribune = Organization.objects.create(
            name = 'The Tribune Corporation',
            slug = 'tribune',
            headquarters = chicago,
        )
        latimes = Organization.objects.create(
            name = 'Los Angeles Times',
            slug = 'los-angeles-times',
            headquarters = los_angeles,
            parent = tribune,
        )
        reporter = Position.objects.create(
            name = 'Metro Reporter',
            slug = 'metro-reporter',
            organization = latimes
        )
        ruben_salazar = Person.objects.create(
            first_name = 'Rubén',
            last_name = 'Salazar',
            slug = 'ruben-salazar',
            gender = 'M',
            birth_date = '1928-03-03',
            date_of_death = '1970-08-29',
            birth_place = ciudad_juarez,
            entry = "A reporter for the Los Angeles Times",
            is_public = True,
        )
        ruben_salazar.person_types.add(journalist)
        ruben_salazar.save()
        tenure = Tenure.objects.create(
            position = reporter,
            person = ruben_salazar,
            start_date = '1959-01-01',
            end_date = '1970-08-29'
        )
        # Robert Lopez
        robert_lopez = Person.objects.create(
            first_name = 'Robert',
            last_name = 'Lopez',
            slug = 'robert-lopez',
            gender = 'M',
            birth_place = los_angeles,
            entry = "A reporter for the Los Angeles Times",
            is_public = True,
        )
        robert_lopez.person_types.add(journalist)
        robert_lopez.save()
        tenure = Tenure.objects.create(
            position = reporter,
            person = robert_lopez,
            start_date = '1990-01-01',
        )
        robert_lopez.person_types.add(journalist)
        robert_lopez.save()

        return robert_lopez, ruben_salazar

from a_matter.tests.unittests.model_tests import *
from a_matter.tests.unittests.signal_tests import *
from a_matter.tests.unittests.view_tests import *