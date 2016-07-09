# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-09 08:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('author', models.CharField(max_length=50)),
                ('rating', models.FloatField(default=0)),
                ('description', models.TextField(blank=True, default='')),
                ('ISBN', models.CharField(max_length=20)),
                ('publisher', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='BookEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('borrowed', models.BooleanField(default=False)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='books.Book')),
                ('library', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Library')),
            ],
        ),
        migrations.CreateModel(
            name='BookOtherInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('other_info', models.TextField(blank=True)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='books.Book')),
                ('library', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Library')),
            ],
        ),
    ]
