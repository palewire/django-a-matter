from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from a_matter.models import Person

class PersonAdmin(OSMGeoAdmin):
	fieldsets = (
		('Identification', {'fields': ('prefix', 'first_name', 'middle_name', 'last_name', 'suffix', 'nick_name', 'slug', 'gender', 'mugshot', 'mugshot_credit',)}),
		('Origin', 			{'fields': ('birth_date', 'birth_place',)}),
		('Biography', 		{'fields': ('person_type', 'entry',)}),
		('Meta', 			{'fields': ('tags', 'enable_comments', 'is_public',)}),
	)
	list_filter = ('person_type', 'is_public',)
	date_hierarchy = 'birth_date'
	search_fields = ('last_name', 'middle_name', 'first_name',)
	prepopulated_fields = {"slug": ("first_name", "middle_name", "last_name")}
	search_fields = ["first_name", "middle_name", "last_name"]
	# Admin map settings
	layerswitcher = False
	scrollable = False
	map_width = 700
	map_height = 325

admin.site.register(Person, PersonAdmin)

