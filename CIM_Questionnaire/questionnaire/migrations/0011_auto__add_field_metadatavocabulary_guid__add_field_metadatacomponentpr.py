# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MetadataVocabulary.guid'
        db.add_column(u'questionnaire_metadatavocabulary', 'guid',
                      self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True),
                      keep_default=False)

        # Adding field 'MetadataComponentProxy.guid'
        db.add_column(u'questionnaire_metadatacomponentproxy', 'guid',
                      self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MetadataVocabulary.guid'
        db.delete_column(u'questionnaire_metadatavocabulary', 'guid')

        # Deleting field 'MetadataComponentProxy.guid'
        db.delete_column(u'questionnaire_metadatacomponentproxy', 'guid')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'questionnaire.metadatacategorization': {
            'Meta': {'object_name': 'MetadataCategorization'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'registered': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'questionnaire.metadatacomponentproxy': {
            'Meta': {'ordering': "['order']", 'unique_together': "(('vocabulary', 'name'),)", 'object_name': 'MetadataComponentProxy'},
            'documentation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['questionnaire.MetadataComponentProxy']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'vocabulary': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'component_proxies'", 'null': 'True', 'to': "orm['questionnaire.MetadataVocabulary']"})
        },
        'questionnaire.metadatamodel': {
            'Meta': {'object_name': 'MetadataModel'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'component_key': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_document': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_root': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['questionnaire.MetadataModel']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'models'", 'null': 'True', 'to': "orm['questionnaire.MetadataProject']"}),
            'proxy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'models'", 'null': 'True', 'to': "orm['questionnaire.MetadataModelProxy']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'models'", 'null': 'True', 'to': "orm['questionnaire.MetadataVersion']"}),
            'vocabulary_key': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        'questionnaire.metadatamodelcustomizer': {
            'Meta': {'unique_together': "(('name', 'project', 'version', 'proxy'),)", 'object_name': 'MetadataModelCustomizer'},
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'model_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'model_hierarchy_name': ('django.db.models.fields.CharField', [], {'default': "'Component Hierarchy'", 'max_length': '128'}),
            'model_root_component': ('django.db.models.fields.CharField', [], {'default': "'RootComponent'", 'max_length': '128', 'blank': 'True'}),
            'model_show_all_categories': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'model_show_all_properties': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'model_show_hierarchy': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'model_title': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'model_customizers'", 'null': 'True', 'to': "orm['questionnaire.MetadataProject']"}),
            'proxy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.MetadataModelProxy']", 'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'model_customizers'", 'null': 'True', 'to': "orm['questionnaire.MetadataVersion']"}),
            'vocabularies': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['questionnaire.MetadataVocabulary']", 'null': 'True', 'blank': 'True'}),
            'vocabulary_order': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        'questionnaire.metadatamodelproxy': {
            'Meta': {'ordering': "['order']", 'unique_together': "(('version', 'name'),)", 'object_name': 'MetadataModelProxy'},
            'documentation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'package': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'stereotype': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'model_proxies'", 'null': 'True', 'to': "orm['questionnaire.MetadataVersion']"})
        },
        'questionnaire.metadataopenidprovider': {
            'Meta': {'object_name': 'MetadataOpenIDProvider'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        },
        'questionnaire.metadataproject': {
            'Meta': {'object_name': 'MetadataProject'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'authenticated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'providers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['questionnaire.MetadataOpenIDProvider']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'vocabularies': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['questionnaire.MetadataVocabulary']", 'null': 'True', 'blank': 'True'})
        },
        'questionnaire.metadatascientificcategorycustomizer': {
            'Meta': {'ordering': "['order']", 'unique_together': "(('name', 'project', 'proxy', 'vocabulary_key', 'component_key', 'model_customizer'),)", 'object_name': 'MetadataScientificCategoryCustomizer'},
            'component_key': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'model_customizer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'scientific_property_category_customizers'", 'null': 'True', 'to': "orm['questionnaire.MetadataModelCustomizer']"}),
            'model_key': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pending_deletion': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'model_scientific_category_customizers'", 'null': 'True', 'to': "orm['questionnaire.MetadataProject']"}),
            'proxy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.MetadataScientificCategoryProxy']", 'null': 'True', 'blank': 'True'}),
            'vocabulary_key': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        'questionnaire.metadatascientificcategoryproxy': {
            'Meta': {'ordering': "['order']", 'unique_together': "(('component', 'name'),)", 'object_name': 'MetadataScientificCategoryProxy'},
            'component': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'categories'", 'null': 'True', 'to': "orm['questionnaire.MetadataComponentProxy']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'questionnaire.metadatascientificproperty': {
            'Meta': {'ordering': "['order']", 'object_name': 'MetadataScientificProperty'},
            'atomic_value': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'category_key': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'enumeration_other_value': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'enumeration_value': ('CIM_Questionnaire.questionnaire.fields.EnumerationField', [], {'null': 'True', 'blank': 'True'}),
            'extra_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extra_standard_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'extra_units': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enumeration': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_label': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scientific_properties'", 'null': 'True', 'to': "orm['questionnaire.MetadataModel']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'proxy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.MetadataScientificPropertyProxy']", 'null': 'True', 'blank': 'True'})
        },
        'questionnaire.metadatascientificpropertycustomizer': {
            'Meta': {'ordering': "['order']", 'object_name': 'MetadataScientificPropertyCustomizer'},
            'atomic_default': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'atomic_type': ('django.db.models.fields.CharField', [], {'default': "'DEFAULT'", 'max_length': '512', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'scientific_property_customizers'", 'null': 'True', 'to': "orm['questionnaire.MetadataScientificCategoryCustomizer']"}),
            'category_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'component_key': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'default_value': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'display_extra_description': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'display_extra_standard_name': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'display_extra_units': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'displayed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'documentation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'edit_extra_description': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'edit_extra_standard_name': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'edit_extra_units': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'enumeration_choices': ('CIM_Questionnaire.questionnaire.fields.EnumerationField', [], {'null': 'True', 'blank': 'True'}),
            'enumeration_default': ('CIM_Questionnaire.questionnaire.fields.EnumerationField', [], {'null': 'True', 'blank': 'True'}),
            'enumeration_multi': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enumeration_nullable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enumeration_open': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'extra_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extra_standard_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'extra_units': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inline_help': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_enumeration': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'model_customizer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scientific_property_customizers'", 'null': 'True', 'to': "orm['questionnaire.MetadataModelCustomizer']"}),
            'model_key': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'proxy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.MetadataScientificPropertyProxy']", 'null': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'unique': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'verbose_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'vocabulary_key': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        'questionnaire.metadatascientificpropertyproxy': {
            'Meta': {'ordering': "['order']", 'unique_together': "(('component', 'category', 'name'),)", 'object_name': 'MetadataScientificPropertyProxy'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'scientific_properties'", 'null': 'True', 'to': "orm['questionnaire.MetadataScientificCategoryProxy']"}),
            'choice': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'component': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'scientific_properties'", 'null': 'True', 'to': "orm['questionnaire.MetadataComponentProxy']"}),
            'documentation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_label': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'values': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'questionnaire.metadatasite': {
            'Meta': {'object_name': 'MetadataSite'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'metadata_site'", 'unique': 'True', 'null': 'True', 'to': u"orm['sites.Site']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        'questionnaire.metadatastandardcategorycustomizer': {
            'Meta': {'ordering': "['order']", 'unique_together': "(('name', 'project', 'proxy', 'model_customizer'),)", 'object_name': 'MetadataStandardCategoryCustomizer'},
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'model_customizer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'standard_property_category_customizers'", 'null': 'True', 'to': "orm['questionnaire.MetadataModelCustomizer']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pending_deletion': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'model_standard_category_customizers'", 'null': 'True', 'to': "orm['questionnaire.MetadataProject']"}),
            'proxy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.MetadataStandardCategoryProxy']", 'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'model_standard_category_customizers'", 'null': 'True', 'to': "orm['questionnaire.MetadataVersion']"})
        },
        'questionnaire.metadatastandardcategoryproxy': {
            'Meta': {'ordering': "['order']", 'unique_together': "(('categorization', 'name'),)", 'object_name': 'MetadataStandardCategoryProxy'},
            'categorization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'categories'", 'to': "orm['questionnaire.MetadataCategorization']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'properties': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'category'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['questionnaire.MetadataStandardPropertyProxy']"})
        },
        'questionnaire.metadatastandardproperty': {
            'Meta': {'ordering': "['order']", 'object_name': 'MetadataStandardProperty'},
            'atomic_value': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'enumeration_other_value': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'enumeration_value': ('CIM_Questionnaire.questionnaire.fields.EnumerationField', [], {'null': 'True', 'blank': 'True'}),
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_label': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'standard_properties'", 'null': 'True', 'to': "orm['questionnaire.MetadataModel']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'proxy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.MetadataStandardPropertyProxy']", 'null': 'True', 'blank': 'True'}),
            'relationship_value': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['questionnaire.MetadataModel']", 'null': 'True', 'blank': 'True'})
        },
        'questionnaire.metadatastandardpropertycustomizer': {
            'Meta': {'ordering': "['order']", 'object_name': 'MetadataStandardPropertyCustomizer'},
            'atomic_type': ('django.db.models.fields.CharField', [], {'default': "'DEFAULT'", 'max_length': '512', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'standard_property_customizers'", 'null': 'True', 'to': "orm['questionnaire.MetadataStandardCategoryCustomizer']"}),
            'category_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'default_value': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'displayed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'documentation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'editable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'enumeration_choices': ('CIM_Questionnaire.questionnaire.fields.EnumerationField', [], {'null': 'True', 'blank': 'True'}),
            'enumeration_default': ('CIM_Questionnaire.questionnaire.fields.EnumerationField', [], {'null': 'True', 'blank': 'True'}),
            'enumeration_multi': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enumeration_nullable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enumeration_open': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inherited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'inline_help': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'model_customizer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'standard_property_customizers'", 'null': 'True', 'to': "orm['questionnaire.MetadataModelCustomizer']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'proxy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.MetadataStandardPropertyProxy']", 'null': 'True', 'blank': 'True'}),
            'relationship_cardinality': ('CIM_Questionnaire.questionnaire.fields.CardinalityField', [], {'max_length': '8', 'blank': 'True'}),
            'relationship_show_subform': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'subform_customizer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'property_customizer'", 'null': 'True', 'to': "orm['questionnaire.MetadataModelCustomizer']"}),
            'suggestions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'unique': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'verbose_name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'questionnaire.metadatastandardpropertyproxy': {
            'Meta': {'ordering': "['order']", 'unique_together': "(('model_proxy', 'name'),)", 'object_name': 'MetadataStandardPropertyProxy'},
            'atomic_default': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'atomic_type': ('django.db.models.fields.CharField', [], {'default': "'DEFAULT'", 'max_length': '64'}),
            'documentation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enumeration_choices': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enumeration_multi': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enumeration_nullable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enumeration_open': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_label': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'model_proxy': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'standard_properties'", 'null': 'True', 'to': "orm['questionnaire.MetadataModelProxy']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'relationship_cardinality': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'relationship_target_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.MetadataModelProxy']", 'null': 'True', 'blank': 'True'}),
            'relationship_target_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'})
        },
        'questionnaire.metadatauser': {
            'Meta': {'object_name': 'MetadataUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'projects': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'metadata_user'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['questionnaire.MetadataProject']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'metadata_user'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        'questionnaire.metadataversion': {
            'Meta': {'object_name': 'MetadataVersion'},
            'categorization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'versions'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['questionnaire.MetadataCategorization']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'registered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'questionnaire.metadatavocabulary': {
            'Meta': {'object_name': 'MetadataVocabulary'},
            'document_type': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'registered': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['questionnaire']