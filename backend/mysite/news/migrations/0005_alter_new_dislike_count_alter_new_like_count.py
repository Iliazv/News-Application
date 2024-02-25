# Generated by Django 5.0.2 on 2024-02-25 13:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_new_dislike_count_new_like_count'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='new',
            name='dislike_count',
            field=models.ManyToManyField(blank=True, related_name='new_dislikes', to=settings.AUTH_USER_MODEL, verbose_name='Количество дизлайков'),
        ),
        migrations.AlterField(
            model_name='new',
            name='like_count',
            field=models.ManyToManyField(blank=True, related_name='new_likes', to=settings.AUTH_USER_MODEL, verbose_name='Количество лайков'),
        ),
    ]