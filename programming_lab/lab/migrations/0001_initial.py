# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Lab'
        db.create_table('lab_lab', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('project_type', self.gf('django.db.models.fields.CharField')(default='Other', max_length=32)),
        ))
        db.send_create_signal('lab', ['Lab'])


    def backwards(self, orm):
        
        # Deleting model 'Lab'
        db.delete_table('lab_lab')


    models = {
        'lab.lab': {
            'Meta': {'object_name': 'Lab'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'project_type': ('django.db.models.fields.CharField', [], {'default': "'Other'", 'max_length': '32'})
        }
    }

    complete_apps = ['lab']
