from django.conf.urls.defaults import *

urlpatterns = patterns('a_matter.views',
	# Index
	url(r'^$', 'index', name='site-index'),
	# Lists
	url(r'^organization/list/$', 'organization_list', name='organization-list'),
	url(r'^position/list/$', 'position_list', name='position-list'),
	url(r'^person-type/list/$', 'person_type_list', name='person-type-list'),
	# Details
	url(r'^organization/(?P<slug>[-\w]+)/$', 'organization_detail', name='organization-detail'),
)