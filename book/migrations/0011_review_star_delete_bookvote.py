# Generated by Django 5.0.3 on 2024-04-12 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0010_alter_doubanreview_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='star',
            field=models.IntegerField(null=True, verbose_name='评分'),
        ),
        migrations.DeleteModel(
            name='BookVote',
        ),
    ]
