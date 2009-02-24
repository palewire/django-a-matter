from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from tagging.fields import TagField

import datetime
import dateutil


class PersonType(models.Model):
	name = models.CharField(_('name'), max_length=100)
	slug = models.SlugField(_('slug'), unique=True)

	class Meta:
		verbose_name = _('person type')
		ordering = ('name',)

	def __unicode__(self):
		return self.name


class Organization(models.Model):
	name = models.CharField(max_length=100)
	slug = models.SlugField(unique=True)
	parent = models.ForeignKey('self', null=True, blank=True, help_text=_('The organization that controls this one.'))
	headquarters = models.ForeignKey('places.Place', blank=True, null=True, help_text=_('The location of this organization\'s headquarters.'))
	employee_count = models.IntegerField(default=0, help_text=_('The total number of biographies published about current employees.'))
	alumni_count = models.IntegerField(default=0, help_text=_('The total number of biographies published about former employees'))

	class Meta:
		ordering = ('name',)
		
	def __unicode__(self):
		self.name
		
	def count_employees(self):
		positions = self.position_set.all()
		occupied_positions = Tenure.objects.filter(position=positions, end_date__isnull=True)
		employees = occupied_positions.person_set.all()
		return employees.count()

	def count_alumni(self):
		positions = self.position_set.all()
		ended_tenures = Tenure.objects.filter(position=positions, end_date__isnull=False)
		alumni = ended_tenures.person_set.all()
		return alumni.count()


class Position(models.Model):
	name = models.CharField(max_length=100)
	slug = models.SlugField(unique=True)
	organization = models.ForeignKey(Organization)

	def current_occupant(self):
		try:
			return Tenure.objects.get(position=self, end_date__isnull=True)
		except Tenure.MultipleObjectsReturned:
			raise u'More than one current occupant'
		
	def previous_occupants(self, count=5):
		previous_occupants = Tenure.objects.filter(position=self, end_date__isnull=False).order_by('-end_date')
		return previous_occupants[count]


class Tenure(models.Model):
	position = models.ForeignKey(Position)
	person = models.ForeignKey(Person)
	start_date = models.DateField()
	end_date = models.DateField(null=True, blank=True)


class Person(models.Model):
	"""
	A biographical entry about a newsworthy person.
	"""
	GENDER_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
	)
	# Indentifers
	prefix = models.CharField(_('title or honorary prefix'), blank=True, null=True, max_length=10))
	first_name = models.CharField(_('first name'), blank=True, null=True, max_length=100)
	middle_name = models.CharField(_('middle name'), blank=True, null=True, max_length=100)
	last_name = models.CharField(_('last name'), blank=True, null=True, max_length=100)
	suffix = models.CharField(_('suffix'), blank=True, null=True, max_length=10)
	slug = models.SlugField(_('slug'), unique=True)
	gender = models.CharField(_('gender'), choices=GENDER_CHOICES, blank=True, null=True, max_length=1)
	mugshot = models.FileField(_('mugshot'), upload_to='mugshots', blank=True)
	mugshot_credit = models.CharField(_('mugshot credit'), blank=True, max_length=200)

	# Origin
	birth_date = models.DateField(_('birth date'), blank=True, null=True)
	birth_place = models.ForeignKey('places.Place', blank=True, null=True)

	# Biography
	person_type = models.ManyToManyField(PersonType, blank=True, null=True)
	positions = models.ManyToManyField(Position, blank=True, null=True, through='Tenure')
	entry = models.TextField(_('Biographical entry') help_text=_('reST markup expected.'))

	# Meta
	enable_comments = models.BooleanField(default=True)
	tags = TagField(null=True, blank=True)

	class Meta:
		verbose_name = _('person')
		verbose_name_plural = _('people')
		ordering = ('last_name', 'first_name',)

	def __unicode__(self):
		return u'%s %s' % (self.first_name, self.last_name)

	def age(self):
		TODAY = datetime.date.today()
		return u'%s' % dateutil.relativedelta(TODAY, self.birth_date).years