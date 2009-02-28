# -*- coding: utf-8 -*-
from django.test import TestCase

from a_matter.models import *
from places.models import *

from django.contrib.gis.geos import Point

from django.utils.encoding import smart_unicode

# Helper base class for changes tests that need data.
class AMatterTestCase(TestCase):
    
    def createRuben(self):
        ciudad_juarez = Place.objects.create(
            name = 'Ciudad Juarez',
            slug = 'ciudad-juarez',
            description = 'A city in Chihuahua, Mexico',
            point = Point(31.63722222, -106.42861111)
        )
        journalist = PersonType.objects.create(
            name = 'Journalist',
            slug = 'journalist',
        )
        latimes = Organization.objects.create(
            name = 'Los Angeles Times',
            slug = 'los-angeles-times',
        )
        reporter = Position.objects.create(
            name = 'Reporter',
            slug = 'reporter',
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

        return ruben_salazar

from a_matter.tests.unittests.model_tests import *