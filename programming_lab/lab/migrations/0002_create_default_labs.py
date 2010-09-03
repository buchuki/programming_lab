# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        orm.Lab.objects.create(name="Web Lab", project_type="HTML")
        orm.Lab.objects.create(name="Java Lab", project_type="Java")
        orm.Lab.objects.create(name="C++ Lab", project_type="C")


    def backwards(self, orm):
        "Write your backwards methods here."


    models = {
        'lab.lab': {
            'Meta': {'object_name': 'Lab'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'project_type': ('django.db.models.fields.CharField', [], {'default': "'Other'", 'max_length': '32'})
        }
    }

    complete_apps = ['lab']
