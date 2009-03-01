from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from a_matter.models import *

class TenureInline(admin.TabularInline):
	model = Tenure

class PersonAdmin(OSMGeoAdmin):
	fieldsets = (
		('Identification', {'fields': ('prefix', 'first_name', 'middle_name', 'last_name', 'suffix', 'nickname', 'slug', 'gender', 'mugshot', 'mugshot_credit',)}),
		('Origin',			{'fields': ('birth_date', 'birth_place',)}),
		('Biography',		{'fields': ('person_types', 'entry',)}),
		('Meta',			{'fields': ('tags', 'enable_comments', 'is_public',)}),
	)
	inlines = [
		TenureInline,
	]
	list_display = ('get_full_name', 'get_person_types')
	list_filter = ('person_types', 'gender', 'is_public',)
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

class PersonTypeAdmin(OSMGeoAdmin):
	prepopulated_fields = {"slug": ("name",)}

admin.site.register(PersonType, PersonTypeAdmin)


class PositionAdmin(OSMGeoAdmin):
	prepopulated_fields = {"slug": ("name",)}

admin.site.register(Position, PositionAdmin)


class OrganizationAdmin(OSMGeoAdmin):
	prepopulated_fields = {"slug": ("name",)}

admin.site.register(Organization, OrganizationAdmin)








