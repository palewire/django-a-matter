# -*- coding: utf-8 -*-
from a_matter.tests import AMatterTestCase
from a_matter.models import *

class AMatterSignalTests(AMatterTestCase):

	def testCounts(self):
		"""
		Test that signals work properly.
		"""
		robert, ruben = self.createReporters()
		self.assertEqual(PersonType.objects.get(name='Journalist').person_count, 2)
		self.assertEqual(Organization.objects.get(name='Los Angeles Times').employee_count, 1)
		self.assertEqual(Organization.objects.get(name='Los Angeles Times').alumni_count, 1)
		self.assertEqual(Organization.objects.get(name='The Tribune Corporation').employee_count, 1)
		self.assertEqual(Organization.objects.get(name='The Tribune Corporation').alumni_count, 1)
