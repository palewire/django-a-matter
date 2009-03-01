from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
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
	return object_list(request, queryset = Position.objects.all(),
						template_name = 'demo/position_list.html',
						extra_context = {'angle': 'Position'})

def person_type_list(request):
	return object_list(request, queryset = PersonType.objects.all(),
						template_name = 'demo/person_type_list.html',
						extra_context = {'angle': 'Person Type'})


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
