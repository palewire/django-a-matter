from django.db.models import signals
from django.dispatch import dispatcher

def update_counts(sender, instance, signal, *args, **kwargs):
	"""
	Runs through all the models and updates counts.
	"""
	from a_matter.models import PersonType, Organization
	
	for person_type in PersonType.objects.all():
		person_type.person_count = person_type.count_people()
		person_type.save()
	
	for organization in Organization.objects.all():
		organization.employee_count = organization.count_employees()
		organization.alumni_count = organization.count_alumni()
		organization.save()