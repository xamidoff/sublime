# Generated by Django 4.1 on 2022-09-09 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Kategoriya')),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories/', verbose_name='Rasm')),
                ('slug', models.SlugField(null=True, unique=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategory', to='store.category', verbose_name='Kategoriya')),
            ],
            options={
                'verbose_name': 'Kategoriya',
                'verbose_name_plural': 'Kategoriyalar',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Tovar nomi')),
                ('brand', models.CharField(max_length=255, verbose_name='Modeli')),
                ('performance', models.TextField(default="Hozircha ma'lumot mavjud emas!", verbose_name='Tehnik tavsifi')),
                ('colour', models.CharField(max_length=255, verbose_name='Rangi')),
                ('memory', models.CharField(max_length=255, verbose_name='Xotirasi')),
                ('camera', models.CharField(max_length=255, verbose_name='Kamera')),
                ('battery', models.CharField(max_length=255, verbose_name='Batareya hajmi')),
                ('manufacture_date', models.IntegerField(verbose_name='Ishlab chiqarilgan yili')),
                ('price', models.FloatField(verbose_name='Narxi')),
                ('discount', models.FloatField(blank=True, null=True, verbose_name='Chegirma')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Kiritilgan vaqti')),
                ('quantity', models.IntegerField(default=0, verbose_name='Soni')),
                ('description', models.TextField(default="Hozircha ma'lumot mavjud emas!", verbose_name='Malumot')),
                ('slug', models.SlugField(null=True, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.category', verbose_name='Kategoriya')),
            ],
            options={
                'verbose_name': 'Tovar',
                'verbose_name_plural': 'Tovarlar',
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/', verbose_name='Rasm')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='store.product')),
            ],
            options={
                'verbose_name': 'Rasm',
                'verbose_name_plural': 'Rasmlar',
            },
        ),
    ]
