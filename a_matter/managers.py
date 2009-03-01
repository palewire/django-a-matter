from django.db import models
from django.dispatch import dispatcher
from django.db.models import Q

class PositionManager(models.Manager):

  def live(self):
    """
    All those linked to people who have been approved for publication.
    """
    return self.get_query_set().filter(Q(current_occupant_count__gt=0) | Q(previous_occupant_count__gt=0))


class TenureManager(models.Manager):
 
  def active(self):
    """
    All currently active tenures.
    """
    return self.get_query_set().filter(end_date__isnull=True)


class PersonManager(models.Manager):

  def live(self):
    """
    All entries approved for publication.
    """
    return self.get_query_set().filter(is_public=True)