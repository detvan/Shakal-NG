# -*- coding: utf-8 -*-

from django import template
from shakal.news.models import News

register = template.Library()

@register.inclusion_tag('news/block_news_list.html', takes_context = True)
def news_frontpage(context):
	return {'news': News.news.all().attributes_for_user(context['request'].user)[:10] }
