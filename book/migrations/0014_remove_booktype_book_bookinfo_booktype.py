# Generated by Django 5.0.3 on 2024-04-12 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0013_booktype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booktype',
            name='book',
        ),
        migrations.AddField(
            model_name='bookinfo',
            name='booktype',
            field=models.ManyToManyField(to='book.booktype'),
        ),
    ]