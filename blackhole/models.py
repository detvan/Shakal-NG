# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from mptt.models import MPTTModel, TreeForeignKey

from comments.models import RootHeader, Comment
from common_utils.models import TimestampModelMixin
from rich_editor.fields import RichTextOriginalField, RichTextFilteredField


@python_2_unicode_compatible
class VocabularyNodeType(models.Model):
	name = models.CharField(max_length=32, db_column='type')

	def __str__(self):
		return self.name


@python_2_unicode_compatible
class Term(MPTTModel, models.Model):
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
	vocabulary = models.ForeignKey(VocabularyNodeType, db_column='vid')
	name = models.CharField(max_length=255)
	description = models.TextField()

	@models.permalink
	def get_absolute_url(self):
		return ('blackhole:story_list_term', (self.pk,), {})

	def __str__(self):
		return self.name


@python_2_unicode_compatible
class Node(TimestampModelMixin, models.Model):
	node_type = models.CharField(max_length=32)
	title = models.CharField(max_length=128)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
	revision = models.ForeignKey('blackhole.NodeRevision', related_name='revisions')
	is_published = models.BooleanField(blank=True, default=False)
	is_commentable = models.BooleanField(blank=True, default=True)
	is_promoted = models.BooleanField(blank=True, default=False)
	is_sticky = models.BooleanField(blank=True, default=False)
	terms = models.ManyToManyField('blackhole.Term', blank=True)

	comments_header = GenericRelation(RootHeader, related_query_name='blackhole_node')
	comments = GenericRelation(Comment, related_query_name='blackhole_node')

	class Meta:
		verbose_name = 'blackhole článok'
		verbose_name_plural = 'blackhole články'

	@models.permalink
	def get_absolute_url(self):
		return ('blackhole:story_detail', (self.pk,), {})

	def __str__(self):
		return self.title


@python_2_unicode_compatible
class NodeRevision(TimestampModelMixin, models.Model):
	node = models.ForeignKey('blackhole.Node')
	author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
	title = models.CharField(max_length=128)
	original_body = RichTextOriginalField(
		filtered_field='filtered_body',
		property_name='body',
		parsers={'raw': '', 'html': 'full'}
	)
	filtered_body = RichTextFilteredField()
	log = models.TextField(blank=True)

	def __str__(self):
		return self.title


@python_2_unicode_compatible
class File(models.Model):
	node = models.ForeignKey('blackhole.Node')
	filename = models.CharField(max_length=255)
	filepath = models.FileField(upload_to='blackhole')
	filemime = models.CharField(max_length=255)
	filesize = models.IntegerField()

	def __str__(self):
		return self.filename
