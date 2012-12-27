# -*- coding: utf-8 -*-

from attachment.models import Attachment
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta
from shakal.threaded_comments.models import RootHeader, CommentCountManager

class Section(models.Model):
	name = models.CharField(max_length = 255, verbose_name = _('name'))
	slug = models.SlugField(unique = True)
	description = models.TextField(verbose_name = _('description'))

	def clean(self):
		slug_num = None
		try:
			slug_num = int(self.slug)
		except:
			pass
		if slug_num is not None:
			raise ValidationError(_('Numeric slug values are not allowed'))

	@permalink
	def get_absolute_url(self):
		return ('forum:section', None, {'section': self.slug})

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = _('section')
		verbose_name_plural = _('sections')


class TopicManager(models.Manager):
	def get_query_set(self):
		return super(TopicManager, self).get_query_set().select_related('user', 'section')


class TopicListManager(CommentCountManager):
	def _generate_query_set(self, extra_filter = '', extra_params = [], order = None, reverse = False):
		model_definition, query = self._generate_query(Topic, reverse = reverse, skip = set(('user', 'section', )))
		params = extra_params
		if extra_filter:
			query += ' WHERE '+extra_filter
		if order == '-last_comment':
			query += ' ORDER BY "'+RootHeader._meta.db_table+'"."last_comment" DESC'
		elif order == '-pk':
			if reverse:
				query += ' ORDER BY "'+RootHeader._meta.db_table+'"."id" DESC'
			else:
				query += ' ORDER BY "'+Topic._meta.db_table+'"."id" DESC'
		elif order == '-comment_count':
			query += ' ORDER BY "'+RootHeader._meta.db_table+'"."comment_count" DESC'
		return super(TopicListManager, self).get_raw_query_set(query, model_definition = model_definition, params = params)

	def newest_topics(self, section = None):
		queryset = self.get_prefetch_query_set()
		if not section is None:
			queryset = queryset.filter(section = section)
		queryset = queryset.order_by('-pk')
		return queryset

	def newest_comments(self):
		return self._generate_query_set(order = '-last_comment', reverse = True)

	def no_comments(self):
		table = RootHeader._meta.db_table
		return self._generate_query_set(
			extra_filter = '"'+table+'"."comment_count" = %s AND "'+table+'"."last_comment" > %s',
			extra_params = [0, datetime.now() - timedelta(60)],
			order = '-pk',
			reverse = True
		)

	def most_commented(self):
		table = RootHeader._meta.db_table
		return self._generate_query_set(
			extra_filter = '"'+table+'"."last_comment" > %s',
			extra_params = [datetime.now() - timedelta(30)],
			order = '-comment_count'
		)


class Topic(models.Model):
	objects = TopicManager()
	topics = TopicListManager()

	section = models.ForeignKey(Section, verbose_name = _('section'))
	subject = models.CharField(max_length = 100, verbose_name = _('subject'))
	text = models.TextField(verbose_name = _('text'))
	time = models.DateTimeField(default = datetime.now, verbose_name = _('time'))
	authors_name = models.CharField(max_length = 50, blank = False, verbose_name = _('authors name'))
	author = models.ForeignKey(User, blank = True, null = True, verbose_name = _('author'))
	comments_header = generic.GenericRelation(RootHeader)
	breadcrumb_label = _('forum')
	attachments = generic.GenericRelation(Attachment)

	def get_authors_name(self):
		if self.author:
			if self.author.get_full_name():
				return self.author.get_full_name()
			else:
				return self.author.username
		else:
			return self.authors_name
	get_authors_name.short_description = _('user name')

	@permalink
	def get_absolute_url(self):
		return ('forum:topic-detail', None, {'pk': self.pk})

	@permalink
	def get_list_url(self):
		return ('forum:overview', None, None)

	def __unicode__(self):
		return self.subject

	class Meta:
		verbose_name = _('topic')
		verbose_name_plural = _('topics')
