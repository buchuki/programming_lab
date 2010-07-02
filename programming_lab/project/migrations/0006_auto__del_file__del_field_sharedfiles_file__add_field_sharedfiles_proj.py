# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Removing unique constraint on 'SharedFiles', fields ['shared_with', 'file']
        db.delete_unique('project_sharedfiles', ['shared_with_id', 'file_id'])

        # Deleting model 'File'
        db.delete_table('project_file')

        # Deleting field 'SharedFiles.file'
        db.delete_column('project_sharedfiles', 'file_id')

        # Adding field 'SharedFiles.project'
        db.add_column('project_sharedfiles', 'project', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['project.Project']), keep_default=False)

        # Adding field 'SharedFiles.filename'
        db.add_column('project_sharedfiles', 'filename', self.gf('django.db.models.fields.CharField')(default='', max_length=128), keep_default=False)

        # Adding unique constraint on 'SharedFiles', fields ['project', 'shared_with', 'filename']
        db.create_unique('project_sharedfiles', ['project_id', 'shared_with_id', 'filename'])
    
    
    def backwards(self, orm):
        
        # Adding model 'File'
        db.create_table('project_file', (
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project.Project'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contents', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('project', ['File'])

        # Adding field 'SharedFiles.file'
        db.add_column('project_sharedfiles', 'file', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['project.File']), keep_default=False)

        # Deleting field 'SharedFiles.project'
        db.delete_column('project_sharedfiles', 'project_id')

        # Deleting field 'SharedFiles.filename'
        db.delete_column('project_sharedfiles', 'filename')

        # Adding unique constraint on 'SharedFiles', fields ['shared_with', 'file']
        db.create_unique('project_sharedfiles', ['shared_with_id', 'file_id'])

        # Removing unique constraint on 'SharedFiles', fields ['project', 'shared_with', 'filename']
        db.delete_unique('project_sharedfiles', ['project_id', 'shared_with_id', 'filename'])
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'classlist.classlist': {
            'Meta': {'object_name': 'ClassList'},
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'class_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'instructed_classes'", 'null': 'True', 'to': "orm['auth.User']"}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'classes'", 'blank': 'True', 'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'project.project': {
            'Meta': {'object_name': 'Project'},
            'classlist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classlist.ClassList']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'project.sharedfiles': {
            'Meta': {'unique_together': "(('project', 'filename', 'shared_with'),)", 'object_name': 'SharedFiles'},
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['project.Project']"}),
            'shared_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'shared_with': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }
    
    complete_apps = ['project']
