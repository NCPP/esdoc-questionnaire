
####################
#   Django-CIM-Forms
#   Copyright (c) 2012 CoG. All rights reserved.
#
#   Developed by: Earth System CoG
#   University of Colorado, Boulder
#   http://cires.colorado.edu/
#
#   This project is distributed according to the terms of the MIT license [http://www.opensource.org/licenses/MIT].
####################

__author__="allyn.treshansky"
__date__ ="Jun 11, 2013 11:39:24 AM"

"""
.. module:: views_edit

Summary of module goes here

"""

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, FieldError, MultipleObjectsReturned
from django.core.urlresolvers import reverse
from django.http import *
from django.shortcuts import *

from dcf.utils  import *
from dcf.models import *
from dcf.forms  import *
from dcf.views.views_error import error as dcf_error

def find_component_parent(component_name,component_collection,parent=None):
    """
    searches the component tree for a given component and returns its parent
    component tree is an arbitrarily complex dictionary of lists of dictionaries of lists...
    """
    if isinstance(component_collection,dict):
        for key,value in component_collection.iteritems():
            if key.lower() == component_name.lower():
                return parent
            if isinstance(value,list):
                for v in value:
                    parent = find_component_parent(component_name,v,key)
                    if parent is not None:
                        return parent


def check_parameters(request,version_number="",project_name="",model_name=""):

    # try to get the requested project...
    try:
        project = MetadataProject.objects.get(name__iexact=project_name)
    except ObjectDoesNotExist:
        msg = "Cannot find the project '%s'.  Has it been registered?" % project_name
        return dcf_error(request,msg)

    # try to get the requested version...
    if version_number:
        try:
            version = MetadataVersion.objects.get(name__iexact=METADATA_NAME,number=version_number)
        except ObjectDoesNotExist:
            msg = "Cannot find version '%s_%s'.  Has it been registered?" % (METADATA_NAME,version_number)
            return dcf_error(request,msg)
    else:
        version = project.getDefaultVersion()
        if not version:
            msg = "please specify a version; the '%s' project has no default one." % project.getName()
            return dcf_error(request,msg)

    # try to get the default customizer for this project/version/model...
    try:
        customizer = MetadataModelCustomizer.objects.get(project=project,version=version,model=model_name,default=1)
    except MetadataModelCustomizer.DoesNotExist:
        msg = "There is no default customization associated with '%s'" % (model_name)
        return dcf_error(request,msg)

    # get the default categorization and vocabulary...
    categorizations = version.categorizations.all()
    vocabularies = project.vocabularies.all()
    # TODO: THIS IS CLEARLY DUMB,
    # BUT THE RELATEDOBJECTMANAGER IS BEING USED FOR THE TIME WHEN
    # THIS CODE CAN SUPPORT MULTPLE CATEGORIZATIONS
    categorization  = categorizations[0] if categorizations else None
    vocabulary  = vocabularies[0] if vocabularies else None
    if not categorization:
        msg = "There is no default categorization associated with version %s." % version
        return dcf_error(request,msg)
    if not vocabulary:
        msg = "There is no default vocabulary associated with project %s." % project
        return dcf_error(request,msg)

    # try to get the requested model...
    model_class = version.getModelClass(model_name)

    return (project,version,customizer,categorization,vocabulary,model_class)

def edit_existing(request,version_number="",project_name="",model_name="",model_id=""):

    msg = ""

    (project,version,customizer,categorization,vocabulary,model_class) = \
    check_parameters(request,version_number,project_name,model_name)

    try:
        component_tree = vocabulary.getComponentTree()
        component_list = vocabulary.getComponentList()

        if not any(component_list):
            msg = "There is no component hierarchy defined in this vocabulary.  Has it been registered?"
            return dcf_error(request,msg)
    except:
        msg = "There is no component hierarchy defined in this vocabulary.  Has it been registered?"
        return dcf_error(request,msg)

    # try to get the requested model...    
    try:
        model_instance = model_class.objects.get(pk=model_id)
    except ObjectDoesNotExist:
        msg = "Cannot find the specified model.  Please try again."
        return dcf_error(request,msg)
    if not model_instance.isDocument():
        msg = "The model type '%s' is not an editable metadata document" % (model_class.getTitle())
        return dcf_error(request,msg)


    model_instances = {}
    model_instances[model_instance.component_name] = model_instance


    for model in model_instance.getAllChildren():
        model_instances[model.component_name] = model

    form_class = MetadataFormFactory(model_class,customizer)
    
    if request.method == "POST":
    
        model_forms = {}
        for component in component_list:
            component_key = component.lower()
            model_forms[component_key] = form_class(
                request.POST,
                instance=model_instances[component_key],
                prefix=component_key
            )

        validity = []

        for (component_name,model_form) in model_forms.iteritems():
            if model_form.is_valid():
                validity.append(True)
            else:
                validity.append(False)
                print "%s is invalid" % component_name
                print model_form.errors
                print model_form.non_field_errors()

        if all(validity):
            root_component = component_list[0].lower()
            for (component_name,model_form) in model_forms.iteritems():
                model_instances[component_name] = model_form.save(commit=False)
                if ("publish_button" in request.POST) and (component_name.lower() == root_component):
                    model_instances[component_name].published=True
                model_instances[component_name].save()
                model_form.save_m2m()


            
            edit_existing_url = reverse("edit_existing",kwargs={
                "version_number" : version.number,
                "project_name"   : project,
                "model_name"     : model_name,
                "model_id"       : model_instances[root_component].pk,
            }) + "?success=true"
            return HttpResponseRedirect(edit_existing_url)

        else:

            msg = "Unable to save the model.  Please review the form and try again."



    else: # request.method == "GET"

        if request.GET.get("success",False):
            msg = "Successfully saved the model: '%s'." % model_instance.shortName

                
        model_forms = {}
        scientific_property_formsets = {}
        for component in component_list:
            component_key = component.lower()
            model_forms[component_key] = form_class(instance=model_instances[component_key],prefix=component_key)
            scientific_properties = model_instances[component_key].getScientificProperties()
            scientific_property_formsets[component_key] = \
                MetadataScientificPropertyFormSetFactory(
                    queryset    = scientific_properties,
                    prefix      = component_key + "_scientific_property",
                    request     = request,
                )

    standard_categories     = customizer.getStandardCategories()
    scientific_categories   = scientific_categories = vocabulary.categories.all() | project.categories.all()


    # gather all the extra information required by the template
    dict = {
        "msg"                           : msg,
        "forms"                         : model_forms,
        "scientific_property_formsets"  : scientific_property_formsets,
        "standard_categories"           : standard_categories,
        "scientific_categories"         : scientific_categories,
        "customizer"                    : customizer,
        "project"                       : project,
        "version"                       : version,
        "vocabulary"                    : vocabulary,
        "model_class"                   : model_class,
        "component_list"                : component_list,
        "component_tree"                : dict_to_html(component_tree),
    }
    
    return render_to_response('dcf/dcf_edit.html', dict, context_instance=RequestContext(request))



def edit_new(request,version_number="",project_name="",model_name=""):

    msg = ""

    (project,version,customizer,categorization,vocabulary,model_class) = \
    check_parameters(request,version_number,project_name,model_name)

    try:
        component_tree = vocabulary.getComponentTree()
        component_list = vocabulary.getComponentList()
        
        if not any(component_list):
            msg = "There is no component hierarchy defined in this vocabulary.  Has it been registered?"
            return dcf_error(request,msg)
    except:
        msg = "There is no component hierarchy defined in this vocabulary.  Has it been registered?"
        return dcf_error(request,msg)
    
    model_filter_parameters = {
        "metadata_project"   : project,
    }
    if request.method == "GET":
        for (key,value) in request.GET.iteritems():
            key = key + "__iexact"  # this ensures that the filter is case-insenstive
            # bear in mind that if I ever change to using get_or_craete, the filter will have to be case-sensitive
            # see https://code.djangoproject.com/ticket/7789 for more info
            if value.lower()=="true":
                model_filter_parameters[key] = 1
            elif value.lower()=="false":
                model_filter_parameters[key] = 0
            else:
                model_filter_parameters[key] = re.sub('[\"\']','',value) # strip out any quotes

        if len(model_filter_parameters) > 1:
            # if there were (extra) filter parameters passed
            # then try to get the customizer w/ those parameters
            try:
                existing_model_instance = model_class.objects.get(**model_filter_parameters)

                edit_existing_url = reverse("edit_existing",kwargs={
                    "version_number" : version.number,
                    "project_name"   : project.name,
                    "model_name"     : model_name,
                    "model_id"       : existing_model_instance.pk,
                })
                return HttpResponseRedirect(edit_existing_url)

            except FieldError,TypeError:
                # raise an error if some of the filter parameters were invalid
                msg = "Unable to access a '%s' with the following parameters: %s" % (model_class.getTitle(), (", ").join([u'%s=%s'%(key,value) for (key,value) in model_filter_parameters.iteritems()]))
                return dcf_error(request,msg)
            except MultipleObjectsReturned:
                # raise an error if those filter params weren't enough to uniquely identify a customizer
                msg = "Unable to find a <i>single</i> '%s' with the following parameters: %s" % (model_class.getTitle(), (", ").join([u'%s=%s'%(key,value) for (key,value) in model_filter_parameters.iteritems()]))
                return dcf_error(request,msg)
            except MetadataModelCustomizer.DoesNotExist:
                # raise an error if there was no matching query
                msg = "Unable to find any '%s' with the following parameters: %s" % (model_class.getTitle(), (", ").join([u'%s=%s'%(key,value) for (key,value) in model_filter_parameters.iteritems()]))
                return dcf_error(request,msg)

    # if I'm here then I will be working w/ a new model...
    model_instance = model_class(**model_filter_parameters)

    if not model_instance.isDocument():
        msg = "The model type '%s' is not an editable metadata document" % (model_class.getTitle())
        return dcf_error(request,msg)

    form_class = MetadataFormFactory(model_class,customizer)

    if request.method == "POST":

        if "publish_button" in request.POST:
            msg = "Please save the model before publishing it."
            return dcf_error(request,msg)
    
        validity = []

        model_instances                 = {}
        scientific_property_instances   = {}
        model_forms                     = {}
        scientific_property_formsets    = {}

        for component in component_list:
            component_key = component.lower()
            model_filter_parameters.update({"component_name":component_key})
            model_instances[component_key] = model_class(**model_filter_parameters)
            model_forms[component_key] = form_class(
                request.POST,
                instance=model_instances[component_key],
                prefix=component_key
            )

        for component in component_list:
            component_key = component.lower()
            scientific_property_formsets[component_key] = \
                MetadataScientificPropertyFormSetFactory(
                    prefix      = component_key + "_scientific_property",
                    request     = request,  # the factory will pass request.POST as appropriate
                )


        for (component_name,model_form) in model_forms.iteritems():
            if model_form.is_valid():
                validity.append(True)
            else:
                validity.append(False)
                print "%s is invalid" % component_name
                print model_form.errors
                print model_form.non_field_errors()
        for (component_name,scientific_property_formset) in scientific_property_formsets.iteritems():
            if scientific_property_formset.is_valid():
                validity.append(True)
            else:
                validity.append(False)
                print "%s has invalid scientific properties" % component_name
                print scientific_property_formset.errors
                print scientific_property_formset.non_form_errors()


        if all(validity):

            for (component_name,model_form) in model_forms.iteritems():
                model_instances[component_name] = model_form.save(commit=False)
                model_instances[component_name].save()
                model_form.save_m2m()

            for (component_name,scientific_property_formset) in scientific_property_formsets.iteritems():
                scientific_property_instances[component_name] = scientific_property_formset.save()

            for (component_name,model_form) in model_forms.iteritems():

                parent_component = find_component_parent(component_name,component_tree)
                if parent_component:
                    model_instances[component_name].setParent(model_instances[parent_component.lower()])
                model_instances[component_name].addScientificProperties(scientific_property_instances[component_name])
                for scientific_property in scientific_property_instances[component_name]:
                    scientific_property.save()  # have to re-save the component after setting it as a property of the model
                model_instances[component_name].save()
                model_form.save_m2m()
            
            root_component = component_list[0].lower()
            edit_existing_url = reverse("edit_existing",kwargs={
                "version_number" : version.number,
                "project_name"   : project,
                "model_name"     : model_name,
                "model_id"       : model_instances[root_component].pk,
            }) + "?success=true"
            return HttpResponseRedirect(edit_existing_url)

        else:

            msg = "Unable to save the customization.  Please review the form and try again."

            

    else: # request.method == "GET"

        
        model_instances = {}
        model_forms = {}
        for component in component_list:
            component_key = component.lower()
            model_filter_parameters.update({"component_name":component_key})
            model_instances[component_key] = model_class(**model_filter_parameters)
            model_forms[component_key] = form_class(instance=model_instances[component_key],prefix=component_key)

        scientific_property_formsets = {}
        scientific_property_customizers = customizer.getScientificPropertyCustomizers()
        for component in component_list:
            component_key = component.lower()
            scientific_properties = []
            for scientific_property_customizer in scientific_property_customizers.filter(component_name__iexact=component_key):
                scientific_property = MetadataProperty()
                scientific_property.customize(scientific_property_customizer)
                scientific_properties.append(scientific_property)
            initial_scientific_property_data = [
                get_initial_data(scientific_property,{"category" : scientific_property.category, "customizer" : scientific_property.customizer })
                for scientific_property in scientific_properties
            ]
            scientific_property_formsets[component_key] = \
                MetadataScientificPropertyFormSetFactory(
                    initial     = initial_scientific_property_data,
                    extra       = len(initial_scientific_property_data),                    
                    prefix      = component_key + "_scientific_property",
                    request     = request,
                )
            
    standard_categories = customizer.getStandardCategories()
    scientific_categories = scientific_categories = vocabulary.categories.all() | project.categories.all()

    # gather all the extra information required by the template
    dict = {
        "msg"                           : msg,
        "forms"                         : model_forms,
        "scientific_property_formsets"  : scientific_property_formsets,
        "standard_categories"           : standard_categories,
        "scientific_categories"         : scientific_categories,
        "customizer"                    : customizer,
        "project"                       : project,
        "version"                       : version,
        "vocabulary"                    : vocabulary,
        "model_class"                   : model_class,
        "component_list"                : component_list,
        "component_tree"                : dict_to_html(component_tree),
    }


    return render_to_response('dcf/dcf_edit.html', dict, context_instance=RequestContext(request))
