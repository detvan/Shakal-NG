# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.template.response import TemplateResponse
from article.models import Article, Category as ArticleCategory
from forum.models import Topic as ForumTopic

def home(request):
	try:
		top_article = Article.articles.filter(top = True).attributes_for_user(request.user)[0:1][0]
		articles = Article.articles.exclude(pk = top_article.pk).attributes_for_user(request.user)
	except IndexError:
		top_article = None
		articles = Article.articles.attributes_for_user(request.user)

	context = {
		'top_article': top_article,
		'articles': articles[:5],
		'article_categories': ArticleCategory.objects.all(),
		#'forum_new': ForumTopic.topics.newest_comments().all()[:20],
		#'forum_no_comments': ForumTopic.topics.no_comments().order_by('-pk').all()[:5],
		#'forum_most_comments': ForumTopic.topics.most_commented().all()[:5],
	}
	return TemplateResponse(request, "home.html", RequestContext(request, context))
