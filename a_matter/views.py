from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.list_detail import object_list

from a_matter.models import *

def index(request):
	return render_to_response('demo/index.html',
								{})

def organization_list(request):
	return object_list(request, queryset = Organization.objects.all(),
						template_name = 'demo/organization_list.html',
						extra_context = {'angle': 'Organization'})

def position_list(request):
	return object_list(request, queryset = Position.objects.live(),
						template_name = 'demo/position_list.html',
						extra_context = {'angle': 'Position'})

def person_type_list(request):
	return object_list(request, queryset = PersonType.objects.all(),
						template_name = 'demo/person_type_list.html',
						extra_context = {'angle': 'Person Type'})
						
def people_list(request):
	return object_list(request, queryset = Person.objects.live(),
						template_name = 'demo/people_list.html',
						extra_context = {'angle': 'People'})

def organization_detail(request, slug):
	qs = get_object_or_404(Organization, slug=slug)
	return render_to_response('demo/organization_detail.html',
								{'object': qs,
								 'angle': 'Organization',})
								
def position_detail(request, slug):
	qs = get_object_or_404(Position, slug=slug)
	return render_to_response('demo/position_detail.html',
								{'object': qs,
								 'angle': 'Position',})
								
def person_type_detail(request, slug):
	qs = get_object_or_404(PersonType, slug=slug)
	return render_to_response('demo/person_type_detail.html',
								{'object': qs,
								 'angle': 'Person Type',})

def person_detail(request, slug):
	qs = get_object_or_404(Person, slug=slug)
	return render_to_response('demo/person_detail.html',
								{'object': qs,
								 'angle': 'People',})

# Pages
# Recently edited pages
# List of organizations
# List of positions by organization
# List of person types
# List of people alphabetically
# person detail page
# organization detail page
# position detail page
# person type detail page
# Would it be possible to tree out the Organizations by parent child relationships?