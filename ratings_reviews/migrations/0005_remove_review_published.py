# Generated by Django 5.0.2 on 2024-03-09 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratings_reviews', '0004_rename_user_can_delete_review_published'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='published',
        ),
    ]
