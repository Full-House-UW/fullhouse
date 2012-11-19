# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Task.due'
        db.alter_column('dashboard_task', 'due', self.gf('django.db.models.fields.DateTimeField')())

    def backwards(self, orm):

        # Changing field 'Task.due'
        db.alter_column('dashboard_task', 'due', self.gf('django.db.models.fields.CharField')(max_length=10))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'dashboard.announcement': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Announcement'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dashboard.UserProfile']"}),
            'expiration': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'announcements'", 'to': "orm['dashboard.House']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'dashboard.house': {
            'Meta': {'object_name': 'House'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '9'})
        },
        'dashboard.inviteprofile': {
            'Meta': {'object_name': 'InviteProfile'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dashboard.House']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invite_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'sent_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'dashboard.task': {
            'Meta': {'object_name': 'Task'},
            'assigned': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks_assigned'", 'to': "orm['dashboard.UserProfile']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks_created'", 'to': "orm['dashboard.UserProfile']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'due': ('django.db.models.fields.DateTimeField', [], {}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': "orm['dashboard.House']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'dashboard.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'members'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['dashboard.House']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['dashboard']