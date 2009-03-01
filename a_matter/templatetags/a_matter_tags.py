from django import template
from django.utils.translation import ugettext_lazy as _

from django.contrib.contenttypes.models import ContentType

from a_matter.models import *

register = template.Library()


class CareerHistoryNode(template.Node):
	def __init__(self, obj, varname):
		self.obj = template.Variable(obj)
		self.varname = varname

	def render(self, context):
		resolved_obj = self.obj.resolve(context)
		context[self.varname] = \
			Tenure.objects.filter(person=resolved_obj).order_by('-end_date')
		return ''


def do_career_history(parser, token):
	""" 
	Gets a list of all positions held by a particular person.
	
	Syntax::

		{% get_career_history [object] as [varname] %}
	
	Example usage::

		{% load a_matter_tags %}
		{% get_career_history object as career_history %}
		{% for position in career_history %}
		<ul>
			{% for tenure in career_history %}
				<li>{{ tenure.position }}, {{ tenure.start_date }} - {{ tenure.end_date }}</li>
			{% endfor %}
		</ul>
	
	Good for pulling the list into object_detail pages as a sidebar.
		
	"""
	bits = token.contents.split()
	if len(bits) != 4:
		raise template.TemplateSyntaxError (_("get_changes_for_object tag takes exactly four arguments"))
	if bits[2] != 'as':
		raise template.TemplateSyntaxError(_("third argument to %s tag must be 'as'") % bits[0])
	return CareerHistoryNode(bits[1], bits[3])


register.tag('get_career_history', do_career_history)