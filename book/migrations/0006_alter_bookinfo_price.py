# Generated by Django 5.0.3 on 2024-04-10 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_alter_doubanreview_namelogo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinfo',
            name='price',
            field=models.DecimalField(decimal_places=1, max_digits=10, null=True, verbose_name='价格'),
        ),
    ]
