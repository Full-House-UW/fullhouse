# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TaskInstance'
        db.create_table('dashboard_taskinstance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(related_name='instances', to=orm['dashboard.Task'])),
            ('assignee', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tasks_assigned', to=orm['dashboard.UserProfile'])),
            ('completed_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tasks_completed', null=True, to=orm['dashboard.UserProfile'])),
            ('completed_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('due_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('dashboard', ['TaskInstance'])

        # Adding field 'Task.is_active'
        db.add_column('dashboard_task', 'is_active',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Task.frequency'
        db.add_column('dashboard_task', 'frequency',
                      self.gf('django.db.models.fields.CharField')(default='--', max_length=4),
                      keep_default=False)

        # Adding field 'Task.first_due'
        db.add_column('dashboard_task', 'first_due',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 12, 2, 0, 0)),
                      keep_default=False)

        # Adding M2M table for field participants on 'Task'
        db.create_table('dashboard_task_participants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('task', models.ForeignKey(orm['dashboard.task'], null=False)),
            ('userprofile', models.ForeignKey(orm['dashboard.userprofile'], null=False))
        ))
        db.create_unique('dashboard_task_participants', ['task_id', 'userprofile_id'])


        # Changing field 'Task.description'
        db.alter_column('dashboard_task', 'description', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Task.due'
        db.alter_column('dashboard_task', 'due', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Task.assigned'
        db.alter_column('dashboard_task', 'assigned_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['dashboard.UserProfile']))

    def backwards(self, orm):
        # Deleting model 'TaskInstance'
        db.delete_table('dashboard_taskinstance')

        # Deleting field 'Task.is_active'
        db.delete_column('dashboard_task', 'is_active')

        # Deleting field 'Task.frequency'
        db.delete_column('dashboard_task', 'frequency')

        # Deleting field 'Task.first_due'
        db.delete_column('dashboard_task', 'first_due')

        # Removing M2M table for field participants on 'Task'
        db.delete_table('dashboard_task_participants')


        # User chose to not deal with backwards NULL issues for 'Task.description'
        raise RuntimeError("Cannot reverse this migration. 'Task.description' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Task.due'
        raise RuntimeError("Cannot reverse this migration. 'Task.due' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Task.assigned'
        raise RuntimeError("Cannot reverse this migration. 'Task.assigned' and its values cannot be restored.")

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
            'assigned': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'old_tasks_assigned'", 'null': 'True', 'to': "orm['dashboard.UserProfile']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks_created'", 'to': "orm['dashboard.UserProfile']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'due': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'first_due': ('django.db.models.fields.DateField', [], {}),
            'frequency': ('django.db.models.fields.CharField', [], {'default': "'--'", 'max_length': '4'}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': "orm['dashboard.House']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tasks_participating'", 'symmetrical': 'False', 'to': "orm['dashboard.UserProfile']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'dashboard.taskinstance': {
            'Meta': {'object_name': 'TaskInstance'},
            'assignee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks_assigned'", 'to': "orm['dashboard.UserProfile']"}),
            'completed_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks_completed'", 'null': 'True', 'to': "orm['dashboard.UserProfile']"}),
            'completed_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'due_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': "orm['dashboard.Task']"})
        },
        'dashboard.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'members'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['dashboard.House']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['dashboard']