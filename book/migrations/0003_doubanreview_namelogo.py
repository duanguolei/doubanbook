# Generated by Django 5.0.3 on 2024-04-10 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_alter_bookinfo_rating_alter_doubanreview_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='doubanreview',
            name='namelogo',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='评论人头像'),
        ),
    ]