# -*- coding: utf-8 -*-
from a_matter.tests import AMatterTestCase
from a_matter.models import *

from django.utils.encoding import smart_unicode

import datetime

class AMatterModelTests(AMatterTestCase):

	def testSave(self):
		"""
		Test that objects can be successfully saved.
		"""
		robert, ruben = self.createReporters()
		self.failIfEqual(ruben.birth_date, None)
		self.failIfEqual(robert.entry, None)
		self.assertEqual(Person.objects.get(first_name='Rubén', last_name='Salazar'), ruben)
		self.assertEqual(Person.objects.get(first_name='Robert', last_name='Lopez'), robert)

	def testEntryProperties(self):
		"""
		Test that object attributes are returning correctly.
		"""
		robert, ruben = self.createReporters()
		# Person
		self.assertEqual(ruben.first_name, 'Rubén')
		self.assertEqual(ruben.last_name, 'Salazar')
		self.assertEqual(ruben.slug, 'ruben-salazar')
		self.assertEqual(ruben.gender, 'M')
		self.assertEqual(ruben.birth_date, '1928-03-03')
		self.assertEqual(ruben.date_of_death, '1970-08-29')
		self.assertEqual(ruben.entry, "A reporter for the Los Angeles Times")
		self.assertEqual(ruben.is_public, True)
		self.assertEqual(ruben.birth_place.name, 'Ciudad Juarez')
		self.assertEqual(ruben.birth_place.point.wkt, 'POINT (31.6372222200000017 -106.4286111100000056)')
		self.assertEqual(ruben.get_full_name(), 'Rubén Salazar')
		self.assertEqual(ruben.get_person_types(), 'Journalist')
		self.assertEqual(ruben.get_person_types_html(), '<a href="%s">%s</a>' % (PersonType.objects.get(name='Journalist').get_absolute_url(), 'Journalist'))
		self.assertEqual(robert.get_current_positions(), 'Metro Reporter (Los Angeles Times)')
		self.assertEqual(Person.objects.live().count(), 2)
		self.assertEqual(list(Person.objects.live().filter(first_name='Robert')), [robert])
		# PersonType
		self.assertEqual(robert.person_types.all()[0].name, 'Journalist')
		self.assertEqual(robert.person_types.all()[0].count_people(), 2)
		# Position
		self.assertEqual(ruben.positions.all()[0].name, 'Metro Reporter')
		self.assertEqual(ruben.positions.all()[0].has_entry(), False)
		self.assertEqual(list(ruben.positions.all()[0].get_current_occupants()), [Tenure.objects.get(person=robert)])
		self.assertEqual(ruben.positions.all()[0].count_current_occupants(), 1)
		self.assertEqual(list(ruben.positions.all()[0].get_previous_occupants()), [Tenure.objects.get(person=ruben)])
		self.assertEqual(ruben.positions.all()[0].count_previous_occupants(), 1)
		# Organization
		self.assertEqual(ruben.positions.all()[0].organization.name, 'Los Angeles Times')
		self.assertEqual(ruben.positions.all()[0].organization.headquarters.name, 'Los Angeles')
		self.assertEqual(ruben.positions.all()[0].organization.headquarters.point.wkt, 'POINT (34.0000000000000000 -118.2999999999999972)')
		self.assertEqual(ruben.positions.all()[0].organization.parent.name, 'The Tribune Corporation')
		self.assertEqual(ruben.positions.all()[0].organization.parent.headquarters.name, 'Chicago')
		self.assertEqual(ruben.positions.all()[0].organization.parent.headquarters.point.wkt, 'POINT (41.8500000000000014 -87.6500000000000057)')
		self.assertEqual(ruben.positions.all()[0].organization.has_entry(), False)
		self.assertEqual(ruben.positions.all()[0].organization.parent.get_children(), 'Los Angeles Times (1)')
		self.assertEqual(ruben.positions.all()[0].organization.count_employees(), 1)
		self.assertEqual(ruben.positions.all()[0].organization.count_alumni(), 1)
		self.assertEqual(ruben.positions.all()[0].organization.parent.organization_set.all().count(), 1)
		self.assertEqual(ruben.positions.all()[0].organization.parent.organization_set.all()[0].name, 'Los Angeles Times')
		self.assertEqual(ruben.positions.all()[0].organization.parent.organization_set.all()[0].count_employees(), 1)
		self.assertEqual(ruben.positions.all()[0].organization.parent.count_children(), 1)
		self.assertEqual(list(ruben.positions.all()[0].organization.parent.get_children_queryset()), [Organization.objects.get(name='Los Angeles Times')])
		self.assertEqual(ruben.positions.all()[0].organization.parent.get_children(), 'Los Angeles Times (1)')
		self.assertEqual(ruben.positions.all()[0].organization.parent.get_children_html(), '<a href="%s">%s</a>' % (Organization.objects.get(name='Los Angeles Times').get_absolute_url(), 'Los Angeles Times'))
		self.assertEqual(ruben.positions.all()[0].organization.parent.count_employees(), 1)
		self.assertEqual(ruben.positions.all()[0].organization.parent.count_alumni(), 1)
		# Tenure
		self.assertEqual(Tenure.objects.get(person=ruben).is_active(), False)
		self.assertEqual(Tenure.objects.get(person=ruben).__unicode__(), smart_unicode('Metro Reporter Rubén Salazar (Departed)'))
		self.assertEqual(list(Tenure.objects.active()), [Tenure.objects.get(person=robert)])
