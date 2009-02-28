# -*- coding: utf-8 -*-
from a_matter.tests import AMatterTestCase
from a_matter.models import *

class AMatterModelTests(AMatterTestCase):

	def testEntry(self):
		"""
		Tests a typical entry.
		"""
		ruben_salazar = self.createRuben()
		self.assertEqual(Person.objects.get(first_name='Rubén', last_name='Salazar'), ruben_salazar)
		
		