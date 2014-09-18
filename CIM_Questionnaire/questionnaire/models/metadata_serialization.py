
####################
#   CIM_Questionnaire
#   Copyright (c) 2013 CoG. All rights reserved.
#
#   Developed by: Earth System CoG
#   University of Colorado, Boulder
#   http://cires.colorado.edu/
#
#   This project is distributed according to the terms of the MIT license [http://www.opensource.org/licenses/MIT].
####################

__author__="allyn.treshansky"
__date__ ="Dec 18, 2013 1:19:49 PM"

"""
.. module:: questionnaire_serialization

Summary of module goes here

"""

from django.db import models
from django.utils import timezone

from CIM_Questionnaire.questionnaire.utils import APP_LABEL, LIL_STRING, SMALL_STRING, BIG_STRING, HUGE_STRING

class MetadataModelSerialization(models.Model):

    class Meta:
        app_label   = APP_LABEL
        abstract    = False

        unique_together = ("name","version",)

    model = models.ForeignKey("MetadataModel", blank=False, null=False, related_name="serializations")

    name = models.CharField(blank=False, null=False, max_length=LIL_STRING)
    version = models.IntegerField(blank=False)

    publication_date = models.DateTimeField(blank=True, null=True)

    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.publication_date:
            self.publication_date = timezone.now()
        super(MetadataModelSerialization, self).save(*args, **kwargs)
