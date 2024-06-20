# Generated by Django 5.0.3 on 2024-04-10 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinfo',
            name='rating',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='评分'),
        ),
        migrations.AlterField(
            model_name='doubanreview',
            name='rating',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='评分'),
        ),
    ]
