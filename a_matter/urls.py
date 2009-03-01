from django.conf.urls.defaults import *

urlpatterns = patterns('a_matter.views',
	# Index
	url(r'^$', 'index', name='site-index'),
	# Lists
	url(r'^changelog/list/$', 'changelog', name='changelog'),
	url(r'^organization/list/$', 'organization_list', name='organization-list'),
	url(r'^position/list/$', 'position_list', name='position-list'),
	url(r'^person-type/list/$', 'person_type_list', name='person-type-list'),
	url(r'^people/list/$', 'people_list', name='people-list'),
	# Details
	url(r'^organization/(?P<slug>[-\w]+)/$', 'organization_detail', name='organization-detail'),
	url(r'^position/(?P<slug>[-\w]+)/$', 'position_detail', name='position-detail'),
	url(r'^person-type/(?P<slug>[-\w]+)/$', 'person_type_detail', name='person-type-detail'),
	url(r'^people/(?P<slug>[-\w]+)/$', 'person_detail', name='person-detail'),
)