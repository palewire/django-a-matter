from django.test.client import Client

from a_matter.tests import AMatterTestCase
from a_matter.models import *


class AMatterViewTests(AMatterTestCase):
	urls = 'a_matter.urls'
	
	def setUp(self):
		"""
		Setting up the test client for reuse throughout.
		"""
		self.client = Client()

	def testLists(self):
		"""
		Test the generic object_list views.
		"""
		slug_list = ['organization', 'position', 'person-type', 'people', 'changelog']
		for slug in slug_list:
			url = '/%s/list/' % slug
			response = self.client.get(url)
			# Check that the response is 200 OK.
			self.failUnlessEqual(response.status_code, 200)
			
	def testDetails(self):
		"""
		Test the generic object_detail views.
		"""
		robert, ruben = self.createReporters()
		# Index
		url = ''
		response = self.client.get(url)
		self.failUnlessEqual(response.status_code, 200)
		# Organization
		url = ruben.positions.all()[0].organization.get_absolute_url()
		response = self.client.get(url)
		self.failUnlessEqual(response.status_code, 200)
		# Position
		url = robert.positions.all()[0].get_absolute_url()
		response = self.client.get(url)
		self.failUnlessEqual(response.status_code, 200)
		# Person Type
		url = robert.person_types.all()[0].get_absolute_url()
		response = self.client.get(url)
		self.failUnlessEqual(response.status_code, 200)
		# Person
		url = ruben.get_absolute_url()
		response = self.client.get(url)
		self.failUnlessEqual(response.status_code, 200)
		