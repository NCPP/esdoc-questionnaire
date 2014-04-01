
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
__date__ ="Dec 18, 2013 3:49:13 PM"

"""
.. module:: questionnaire_proxy

Summary of module goes here

"""

from django.db import models

#from mptt.models import MPTTModel, TreeForeignKey

from questionnaire.utils import *
from questionnaire.fields import *

### note - following fk fields in __unicode__ method forces queries on the db
### only do that if it's absolutely necessary

class MetadataModelProxy(models.Model):
    class Meta:
        app_label   = APP_LABEL
        abstract    = False
        unique_together = ("version","name")

        # TODO: DELETE THESE NEXT TWO LINES
        verbose_name        = '(DISABLE ADMIN ACCESS SOON) Metadata Model Proxy'
        verbose_name_plural = '(DISABLE ADMIN ACCESS SOON) Metadata Model Proxies'

    name                    = models.CharField(max_length=SMALL_STRING,blank=False,null=False)
    package                 = models.CharField(max_length=SMALL_STRING,blank=True,null=True)
    documentation           = models.TextField(blank=True,null=True)
    order                   = models.PositiveIntegerField(blank=True,null=True)
    version                 = models.ForeignKey("MetadataVersion",blank=False,null=True,related_name="model_proxies")

    def __unicode__(self):
        return u'%s'%(self.name)
        #return u'%s::%s' % (self.version,self.name)

    def get_standard_category_proxies(self):
        if self.version.categorization:
            return self.version.categorization.categories.all().order_by("order")
        else:
            return MetadataStandardCategoryProxy.objects.none()

    @classmethod
    def factory(cls,*args,**kwargs):

        proxy_model_fields = kwargs.pop("fields",{})
        
        (new_model_proxy,created_model) = MetadataModelProxy.objects.get_or_create(**kwargs)
        
        if not created_model:
            # delete all old properties (going to replace them during this registration)...
            old_model_proxy_properties = new_model_proxy.standard_properties.all()
            old_model_proxy_properties.delete()

        property_kwargs = {
            "model_proxy"   : new_model_proxy
        }

        for (new_model_proxy_field_key,new_model_proxy_field_value) in proxy_model_fields.iteritems():
            property_kwargs["name"] = new_model_proxy_field_key
            #new_model_standard_property_proxy = MetadataStandardPropertyProxy()
            (new_model_standard_property_proxy,created_property) = MetadataStandardPropertyProxy.objects.get_or_create(**property_kwargs)
            new_model_standard_property_proxy.save()
        
        # TODO: SHOULD SAVE IT HERE
        # SO THAT I CAN ADD THE PROPERTIES
        # AND SAVE IT AGAIN
        return new_model_proxy

class MetadataPropertyProxy(models.Model):
    class Meta:
        app_label   = APP_LABEL
        abstract    = True

    name                = models.CharField(max_length=BIG_STRING,blank=False,null=False)
    documentation       = models.TextField(blank=True)
    field_type          = models.CharField(max_length=SMALL_STRING,blank=False,null=True,choices=[(ft.getType(),ft.getName()) for ft in MetadataFieldTypes])
    order               = models.PositiveIntegerField(blank=True,null=True)

class MetadataStandardPropertyProxy(MetadataPropertyProxy):
    class Meta:
        app_label   = APP_LABEL
        abstract    = False
        unique_together = ("model_proxy","name")

        # TODO: DELETE THESE NEXT TWO LINES
        verbose_name        = '(DISABLE ADMIN ACCESS SOON) Metadata Standard Property Proxy'
        verbose_name_plural = '(DISABLE ADMIN ACCESS SOON) Metadata Standard Property Proxies'

    model_proxy     = models.ForeignKey("MetadataModelProxy",blank=True,null=True,related_name="standard_properties")


    # attributes for ATOMIC fields
    atomic_default  = models.CharField(max_length=BIG_STRING,blank=True)

    # attributes for ENUMERATION fields
    enumeration_choices  = models.CharField(max_length=HUGE_STRING,blank=True)
    enumeration_open     = models.BooleanField(default=False,blank=True)
    enumeration_multi    = models.BooleanField(default=False,blank=True)
    enumeration_nullable = models.BooleanField(default=False,blank=True)

    # attributes for RELATIONSHIP fields
    relationship_cardinality  = models.CharField(max_length=LIL_STRING,blank=True)
    relationship_target_name  = models.CharField(max_length=BIG_STRING,blank=True)
    relationship_target_model = models.ForeignKey("MetadataModelProxy",blank=True,null=True)
    
    def __unicode__(self):
        return u'%s' % (self.name)
        #return u'%s::%s' % (self.model_proxy,self.name)

    def reset(self):

        if self.field_type == MetadataFieldTypes.ATOMIC:
            pass

        elif self.field_type == MetadataFieldTypes.ENUMERATION:
            pass

        elif self.field_type == MetadataFieldTypes.RELATIONSHIP:
            version     = self.model_proxy.version
            target_name = self.relationship_target_name
            try:
                target_proxy = MetadataModelProxy.objects.get(version=version,name__iexact=target_name)
            except MetadataModelProxy.DoesNotExist:
                msg = "unable to locate model '%s' in version '%s'" % (target_name,version)
                raise QuestionnaireError(msg)

            self.relationship_target_model = target_proxy

        
class MetadataScientificPropertyProxy(MetadataPropertyProxy):
    class Meta:
        app_label   = APP_LABEL
        abstract    = False
        unique_together = ("component","category","name")

        # TODO: DELETE THESE NEXT TWO LINES
        verbose_name        = '(DISABLE ADMIN ACCESS SOON) Metadata Scientific Property Proxy'
        verbose_name_plural = '(DISABLE ADMIN ACCESS SOON) Metadata Scientific Property Proxies'

    component     = models.ForeignKey("MetadataComponentProxy",blank=True,null=True,related_name="scientific_properties")
    category      = models.ForeignKey("MetadataScientificCategoryProxy",blank=True,null=True,related_name="scientific_properties")

    def __unicode__(self):
        #return u'%s::%s::%s' % (self.component,self.category,self.name)
        return u'%s'%(self.name)

class MetadataCategoryProxy(models.Model):
    class Meta:
        app_label   = APP_LABEL
        abstract    = True

    description             = models.TextField(blank=True,null=True)
    order                   = models.PositiveIntegerField(blank=True,null=True)

class MetadataStandardCategoryProxy(MetadataCategoryProxy):
    class Meta:
        app_label   = APP_LABEL
        abstract    = False
        unique_together = ("categorization","name")

        # TODO: DELETE THESE NEXT TWO LINES
        verbose_name        = '(DISABLE ADMIN ACCESS SOON) Metadata Standard Category Proxy'
        verbose_name_plural = '(DISABLE ADMIN ACCESS SOON) Metadata Standard Category Proxies'

    categorization  = models.ForeignKey("MetadataCategorization",blank=False,null=False,related_name="categories")
    properties      = models.ManyToManyField("MetadataStandardPropertyProxy",blank=True,null=True,related_name="category")

    name                    = models.CharField(max_length=BIG_STRING,blank=False,null=False)
    key                     = models.CharField(max_length=BIG_STRING,blank=False,null=False)

    def __unicode__(self):
        return u'%s' % (self.name)

    def has_property(self,standard_property_proxy):
        return standard_property_proxy in self.properties.all()

class MetadataScientificCategoryProxy(MetadataCategoryProxy):
    class Meta:
        app_label   = APP_LABEL
        abstract    = False
        unique_together = ("component","name")


        # TODO: DELETE THESE NEXT TWO LINES
        verbose_name        = '(DISABLE ADMIN ACCESS SOON) Metadata Scientific Category Proxy'
        verbose_name_plural = '(DISABLE ADMIN ACCESS SOON) Metadata Scientific Category Proxies'

    component  = models.ForeignKey("MetadataComponentProxy",blank=True,null=True,related_name="categories")

    name                    = models.CharField(max_length=BIG_STRING,blank=False,null=False)
    key                     = models.CharField(max_length=BIG_STRING,blank=False,null=False)

    def __unicode__(self):
        return u'%s' % (self.name)

    def has_property(self,scientific_property_proxy):
        return scientific_property_proxy in self.properties.all()

@hierarchical
class MetadataComponentProxy(models.Model):
    name                    = models.CharField(max_length=SMALL_STRING,blank=False,null=False)
    documentation           = models.TextField(blank=True,null=True)
    order                   = models.PositiveIntegerField(blank=True,null=True)
    vocabulary              = models.ForeignKey("MetadataVocabulary",blank=False,null=True,related_name="component_proxies")

    class Meta:
        app_label   = APP_LABEL
        abstract    = False
        unique_together = ("vocabulary","name")
        ordering = ['order']

        # TODO: DELETE THESE NEXT TWO LINES
        verbose_name        = '(DISABLE ADMIN ACCESS SOON) Metadata Component Proxy'
        verbose_name_plural = '(DISABLE ADMIN ACCESS SOON) Metadata Component Proxies'

    def __unicode__(self):
        return u'%s'%(self.name)
        #return u'%s::%s' % (self.vocabulary,self.name)
