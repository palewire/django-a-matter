from django.db import models
from django.dispatch import dispatcher
 
class TenureManager(models.Manager):
 
  def active(self):
    """
    All currently active tenures.
    """
    return self.get_query_set().filter(end_date__isnull=True)


class PersonManager(models.Manager):

  def live(self):
    """
    All entries approved for publications.
    """
    return self.get_query_set().filter(is_public=True)