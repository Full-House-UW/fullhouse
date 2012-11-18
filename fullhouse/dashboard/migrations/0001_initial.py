# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'House'
        db.create_table('dashboard_house', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=9)),
        ))
        db.send_create_signal('dashboard', ['House'])

        # Adding model 'InviteProfile'
        db.create_table('dashboard_inviteprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('house', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.House'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('invite_key', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('sent_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('dashboard', ['InviteProfile'])

        # Adding model 'UserProfile'
        db.create_table('dashboard_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True)),
            ('house', self.gf('django.db.models.fields.related.ForeignKey')(related_name='members', null=True, on_delete=models.SET_NULL, to=orm['dashboard.House'])),
        ))
        db.send_create_signal('dashboard', ['UserProfile'])

        # Adding model 'Announcement'
        db.create_table('dashboard_announcement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.UserProfile'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('house', self.gf('django.db.models.fields.related.ForeignKey')(related_name='announcements', to=orm['dashboard.House'])),
        ))
        db.send_create_signal('dashboard', ['Announcement'])


    def backwards(self, orm):
        # Deleting model 'House'
        db.delete_table('dashboard_house')

        # Deleting model 'InviteProfile'
        db.delete_table('dashboard_inviteprofile')

        # Deleting model 'UserProfile'
        db.delete_table('dashboard_userprofile')

        # Deleting model 'Announcement'
        db.delete_table('dashboard_announcement')


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
            'Meta': {'object_name': 'Announcement'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dashboard.UserProfile']"}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'announcements'", 'to': "orm['dashboard.House']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        'dashboard.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'members'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['dashboard.House']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['dashboard']