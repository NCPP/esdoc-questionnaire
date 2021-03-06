__author__="allyn.treshansky"
__date__ ="$Sep 30, 2013 3:11:26 PM$"

from django.template    import *
from django.shortcuts   import *
from django.http        import *

from django.core.urlresolvers   import reverse
from django.contrib             import messages
#from django.contrib.messages    import get_messages

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.models    import get_current_site

from django.views.decorators.debug import sensitive_post_parameters

from views_error        import questionnaire_error as error
from views_help         import questionnaire_help  as help
from views_ajax         import ajax_customize_category, ajax_customize_subform, ajax_select_realization
from views_index        import questionnaire_index as index, questionnaire_project_index as project_index
from views_authenticate import questionnaire_login as login, questionnaire_logout as logout, questionnaire_user as user, questionnaire_register as register
from views_customize    import questionnaire_customize_new as customize_new, questionnaire_customize_existing as customize_existing, questionnaire_customize_help as customize_help
from views_edit         import questionnaire_edit_new as edit_new, questionnaire_edit_existing as edit_existing, questionnaire_edit_help as edit_help
from views_view         import questionnaire_view_new as view_new, questionnaire_view_existing as view_existing, questionnaire_view_help as view_help
from views_feed         import questionnaire_serialize as serialize
from views_test         import test
