# Generated by Django 4.1 on 2022-09-12 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_price_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='publish',
            field=models.BooleanField(default=False, verbose_name='Chop etish'),
        ),
    ]
