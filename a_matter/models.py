from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from tagging.fields import TagField

from django.db.models import signals
from a_matter.signals import update_counts

from a_matter.managers import TenureManager, PersonManager

import datetime


class PersonType(models.Model):
	"""
	A profession or other group a person belongs to.
	
	Examples::
	
		Politician
		Military Officer
		Athlete

	"""
	name = models.CharField(_('name'), max_length=100, help_text=_('100 characters maximum.'))
	slug = models.SlugField(_('slug'), unique=True, help_text=_('For use in URL strings. Must be unique.'))
	description = models.TextField(_('Description of the type.'), null=True, blank=True, help_text=_('reST markup expected. Optional.'))
	person_count = models.IntegerField(default=0, editable=False, help_text=_('The total number of biographies published about this type.'))

	class Meta:
		verbose_name = _('person type')
		ordering = ('name',)

	def __unicode__(self):
		return self.name
		
	def count_people(self):
		return self.person_set.live().count()


class Organization(models.Model):
	"""
	A company, government, NGO or other organization.
	
	Examples::
	
		The United States Government
		The Department of Defense
		The Los Angeles Lakers

	"""
	name = models.CharField(max_length=100, help_text=_('100 characters maximum.'))
	slug = models.SlugField(unique=True, help_text=_('For use in URL strings. Must be unique.'))
	parent = models.ForeignKey('self', null=True, blank=True, help_text=_('The organization that controls this one. Optional.'))
	headquarters = models.ForeignKey('places.Place', blank=True, null=True, help_text=_('The location of this organization\'s headquarters.'))
	entry = models.TextField(_('Description of the organization.'), null=True, blank=True, help_text=_('reST markup expected. Optional.'))
	employee_count = models.IntegerField(default=0, editable=False, help_text=_('The total number of biographies published about current employees.'))
	alumni_count = models.IntegerField(default=0, editable=False, help_text=_('The total number of biographies published about former employees'))

	# Meta
	is_public = models.BooleanField(default=False, help_text=_('If this box is checked, the entry will be published.'))
	enable_comments = models.BooleanField(default=True)
	tags = TagField(null=True, blank=True, help_text=_('Separate tags with spaces. Connect multiple words with dashes. Ex. great-depression-two'))
	created = models.DateTimeField(auto_now_add=True, editable=False)
	last_edited = models.DateTimeField(auto_now=True, editable=False)

	class Meta:
		ordering = ('name',)
		
	def __unicode__(self):
		return self.name
		
	def count_employees(self):
		positions = self.position_set.all()
		occupied_positions = Tenure.objects.filter(position__in=positions, end_date__isnull=True, person__is_public=True)
		employee_count = occupied_positions.count()
		if self.organization_set:
			for child in self.organization_set.all():
				employee_count += child.count_employees()
		return employee_count

	def count_alumni(self):
		positions = self.position_set.all()
		ended_tenures = Tenure.objects.filter(position__in=positions, end_date__isnull=False, person__is_public=True)
		alumni_count = ended_tenures.count()
		if self.organization_set:
			for child in self.organization_set.all():
				alumni_count += child.count_alumni()
		return alumni_count


class Position(models.Model):
	"""
	A job or office.
	
	Examples::
	
		President
		Secretary of Defense
		Shooting Guard

	"""
	name = models.CharField(max_length=100, help_text=_('100 characters maximum.'))
	slug = models.SlugField(unique=True, help_text=_('For use in URL strings. Must be unique.'))
	organization = models.ForeignKey(Organization, null=True, blank=True)
	entry = models.TextField(_('Description of the position.'), null=True, blank=True, help_text=_('reST markup expected. Optional.'))

	# Meta
	is_public = models.BooleanField(default=False, help_text=_('If this box is checked, the entry will be published.'))
	enable_comments = models.BooleanField(default=True)
	tags = TagField(null=True, blank=True, help_text=_('Separate tags with spaces. Connect multiple words with dashes. Ex. great-depression-two'))
	created = models.DateTimeField(auto_now_add=True, editable=False)
	last_edited = models.DateTimeField(auto_now=True, editable=False)
	
	class Meta:
		ordering = ('name',)
		unique_together = ("name", "organization",)

	def __unicode__(self):
		return self.name

	def current_occupants(self):
		return Tenure.objects.filter(position=self, end_date__isnull=True)
		
	def previous_occupants(self):
		previous_occupants = Tenure.objects.filter(position=self, end_date__isnull=False).order_by('-end_date')
		return previous_occupants


class Tenure(models.Model):
	"""
	The period of time that a person holds a position.
	
	Positions without an `end_date` are presumed to be currently occupied.
	
	``Managers``

	``active()``
		The custom manager acrive() returns only changes where `end_date` is null. 

		Example::

			Tenure.objects.active()

	"""
	position = models.ForeignKey(Position)
	person = models.ForeignKey('Person')
	start_date = models.DateField(help_text=_('The date the person started on the job'))
	end_date = models.DateField(null=True, blank=True, help_text=_('The date the person left the job. Leave empty if they currently occupy the position.'))
	objects = TenureManager()
	
	class Meta:
		ordering = ('position', 'person')

	def __unicode__(self): 
		if self.is_active():
			status = 'Active'
		else:
			status = 'Departed'
		return u'%s %s (%s)' % (self.position.name, self.person, status)

	def is_active(self):
		if not self.end_date: 
			return True
		else:
			return False


class Person(models.Model):
	"""
	A biographical entry about a newsworthy person.
	
	Examples::
		
		Barack Obama
		Bob Gates
		Kobe Bryant
	
	``Managers``

	``live()``
		The custom manager live() returns only changes where `is_public` is True. 

		Example::

			Person.objects.live()

	"""
	GENDER_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
	)
	# Identification
	prefix = models.CharField(_('title or honorary prefix'), blank=True, null=True, max_length=10, help_text=_('10 characters maximum.'))
	first_name = models.CharField(_('first name'), max_length=100, help_text=_('100 characters maximum.'))
	middle_name = models.CharField(_('middle name'), blank=True, null=True, max_length=100, help_text=_('100 characters maximum.'))
	last_name = models.CharField(_('last name'), blank=True, null=True, max_length=100, help_text=_('100 characters maximum.'))
	nickname = models.CharField(_('nick name'), blank=True, null=True, max_length=100, help_text=_('100 characters maximum. Optional.'))
	suffix = models.CharField(_('suffix'), blank=True, null=True, max_length=10, help_text=_('10 characters maximum.'))
	slug = models.SlugField(_('slug'), unique=True, help_text=_('For use in URL strings. Must be unique.'))
	gender = models.CharField(_('gender'), choices=GENDER_CHOICES, blank=True, null=True, max_length=1)
	mugshot = models.FileField(_('mugshot'), upload_to='mugshots', blank=True, null=True)
	mugshot_credit = models.CharField(_('mugshot credit'), blank=True, null=True, max_length=200, help_text=_('200 characters maximum.'))

	# Origin
	birth_date = models.DateField(_('birth date'), blank=True, null=True, help_text=_('YYYY-MM-DD format'))
	date_of_death = models.DateField(_('date of death'), blank=True, null=True, help_text=_('YYYY-MM-DD format'))
	birth_place = models.ForeignKey('places.Place', blank=True, null=True, help_text=_('YYYY-MM-DD format'))

	# Biography
	person_types = models.ManyToManyField(PersonType, blank=True, null=True)
	positions = models.ManyToManyField(Position, blank=True, null=True, through='Tenure')
	entry = models.TextField(_('Biographical entry'), help_text=_('reST markup expected.'))

	# Meta
	is_public = models.BooleanField(default=False, help_text=_('If this box is checked, the article will be published.'))
	enable_comments = models.BooleanField(default=True)
	tags = TagField(null=True, blank=True, help_text=_('Separate tags with spaces. Connect multiple words with dashes. Ex. great-depression-two'))
	created = models.DateTimeField(auto_now_add=True, editable=False)
	last_edited = models.DateTimeField(auto_now=True, editable=False)
	objects = PersonManager()

	class Meta:
		verbose_name = _('person')
		verbose_name_plural = _('people')
		ordering = ('last_name', 'first_name',)

	def __unicode__(self):
		return self.get_full_name()
		
	def get_full_name(self):
		"""
		Formats a person's full title as a single string.
		"""
		part_list = [self.prefix, self.first_name, self.middle_name, self.last_name, self.suffix]
		if self.nickname:
			# This is set to present the nickname in quotes.
			# Ex. John "The Jackrabbit" Herbert Dillinger
			part_list.insert(2, '"%s"' % self.nickname)
		# This list comprehension will omit any of the potential name parts that are null.
		full_name = " ".join([i.strip() for i in part_list if i])		
		return full_name
		
# Rerun the totals whenever a Person is saved or deleted.
signals.post_save.connect(update_counts, sender=Person)
signals.post_delete.connect(update_counts, sender=Person)
