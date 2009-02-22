from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import datetime
import dateutil


class PersonType(models.Model):
	name = models.CharField(_('name'), max_length=100)
	slug = models.SlugField(_('slug'), unique=True)

	class Meta:
		verbose_name = _('person type')
		verbose_name_plural = _('person types')
		db_table = 'people_types'
		ordering = ('title',)

	def __unicode__(self):
		return '%s' % self.name


class Person(models.Model):
	"""
	A biographical entry about a particular newsworthy person.
	"""
	GENDER_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
	)
	# Indentifers
	prefix         = models.CharField(_('title or honorary prefix'), blank=True, null=True))
	first_name     = models.CharField(_('first name'), blank=True, null=True, max_length=100)
	middle_name    = models.CharField(_('middle name'), blank=True, null=True, max_length=100)
	last_name      = models.CharField(_('last name'), blank=True, null=True, max_length=100)
	slug           = models.SlugField(_('slug'), unique=True)
	gender         = models.CharField(_('gender'), choices=GENDER_CHOICES, blank=True, null=True, max_length=1)
	
	# Biography
	person_type    = models.ManyToManyField(PersonType, blank=True, null=True)
	positions      = models.ManyToManyField(Position, blank=True, null=True, through='Tenure')
	mugshot        = models.FileField(_('mugshot'), upload_to='mugshots', blank=True)
	mugshot_credit = models.CharField(_('mugshot credit'), blank=True, max_length=200)
	entry          = models.TextField()
	
	# Origin
	birth_date     = models.DateField(_('birth date'), blank=True, null=True)
	birth_place    = models.ForeignKey(Place, blank=True, null=True)
	
	# Meta
	enable_comments = 
	tags = 
	

	class Meta:
		verbose_name = _('person')
		verbose_name_plural = _('people')
		db_table = 'people'
		ordering = ('last_name', 'first_name',)

	def __unicode__(self):
		return u'%s %s' % (self.first_name, self.last_name)

	def age(self):
		TODAY = datetime.date.today()
		return u'%s' % dateutil.relativedelta(TODAY, self.birth_date).years


class Organization(models.Model):
	name = models.CharField(max_length=100)
	slug = models.SlugField(unique=True)
	headquarters = models.ForeignKey(Place, blank=True, null=True)
	employee_count = models.IntegerField(default=0)
	alumni_count = models.IntegerField(default=0)


class Position(models.Model):
	name = models.CharField(max_length=100)
	slug = models.SlugField(unique=True)
	organization = models.ForeignKey(Organization)

	def current_occupant(self):
		
		
	def previous_occupant(self):


class Tenure(models.Model):
	position = models.ForeignKey(Position)
	person = models.ForeignKey(Person)
	start_date = models.DateField()
	end_date = models.DateField(null=True, blank=True)