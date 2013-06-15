# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LongCacheItem'
        db.create_table('dorcx_longcacheitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('value', self.gf('picklefield.fields.PickledObjectField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('dorcx', ['LongCacheItem'])


    def backwards(self, orm):
        # Deleting model 'LongCacheItem'
        db.delete_table('dorcx_longcacheitem')


    models = {
        'dorcx.longcacheitem': {
            'Meta': {'object_name': 'LongCacheItem'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value': ('picklefield.fields.PickledObjectField', [], {})
        }
    }

    complete_apps = ['dorcx']