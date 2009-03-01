from django.template import Template, Context

from a_matter.models import *
from a_matter.tests import AMatterTestCase

class AMatterTemplateTagTests(AMatterTestCase):

    def render(self, t, **c):
        ctx = Context(c)
        out = Template(t).render(ctx)
        return ctx, out

    def testGetCareerHistory(self):
        """
        Tests the tag for pulling a person's career history.
        """
        robert, ruben = self.createReporters()
        t = "{% load a_matter_tags %}{% get_career_history robert as career_history %}"
        match = Tenure.objects.get(person=robert)
        ctx, out = self.render(t, c=match, robert=robert)
        self.assertEqual(out, "")
        self.assertEqual(list(ctx["career_history"]), [match])