# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def create_recomended_articles(main_article, article_list):
    '''
    Creates recommended article objects from article_list
    and _prepends_ to existing recommended articles.
    '''
    from molo.core.models import ArticlePage, ArticlePageRecommendedSections

    existing_recommended_articles = [ra.recommended_article
                                     for ra in main_article.recommended_articles.all()]
    ArticlePageRecommendedSections.objects.filter(page=main_article).delete()

    for hyperlinked_article in article_list:
        ArticlePageRecommendedSections(
            page=main_article,
            recommended_article=hyperlinked_article).save()

    # re-create existing recommended articles
    for article in existing_recommended_articles:
        if article not in article_list:
            ArticlePageRecommendedSections(
                page=main_article,
                recommended_article=article).save()


def convert_articles(apps, schema_editor):
    '''
    Derived from https://github.com/wagtail/wagtail/issues/2110
    '''
    from molo.core.models import ArticlePage
    from wagtail.wagtailcore.blocks import StreamValue

    articles = ArticlePage.objects.all()

    for article in articles:
        stream_data = []
        linked_articles = []
        for block in article.body.stream_data:
            if block['type'] == 'page':
                linked_articles.append(ArticlePage.objects.get(
                                id=block['value']))
            else:
                # add block to new stream_data
                stream_data.append(block)

        if linked_articles:
            create_recomended_articles(article, linked_articles)
            article.get_parent().specific.enable_recommended_section) = True

        stream_block = article.body.stream_block
        article.body = StreamValue(stream_block, stream_data, is_lazy=True)
        article.save()


class Migration(migrations.Migration):

    dependencies = [
        ('gem', '0013_gemsettings_moderator_name'),
    ]

    operations = [
        migrations.RunPython(convert_articles),
    ]
