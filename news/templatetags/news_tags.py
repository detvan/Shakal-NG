# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django_jinja import library
from jinja2 import contextfunction

from news.models import News


@library.global_function
@contextfunction
def news_frontpage(context):
	ctx = {
		'news': News.objects.all()[:10],
		'user': context['user']
	}
	return mark_safe(render_to_string('news/block_news_list.html', ctx))
