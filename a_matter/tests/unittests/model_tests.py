# -*- coding: utf-8 -*-
from a_matter.tests import AMatterTestCase
from a_matter.models import *

import datetime

class AMatterModelTests(AMatterTestCase):

	def testSave(self):
		"""
		Test that objects can be successfully saved.
		"""
		ruben = self.createRuben()
		self.failIfEqual(ruben.birth_date, None)
		self.assertEqual(Person.objects.get(first_name='Rubén', last_name='Salazar'), ruben)

	def testEntryProperties(self):
		"""
		Test that object attributes are returning correctly.
		"""
		ruben = self.createRuben()
		self.assertEqual(ruben.first_name, 'Rubén')
		self.assertEqual(ruben.last_name, 'Salazar')
		self.assertEqual(ruben.slug, 'ruben-salazar')
		self.assertEqual(ruben.gender, 'M')
		self.assertEqual(ruben.birth_date, '1928-03-03')
		self.assertEqual(ruben.date_of_death, '1970-08-29')
		self.assertEqual(ruben.entry, "A reporter for the Los Angeles Times")
