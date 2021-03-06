# Generated by Django 3.0.1 on 2020-03-24 21:54

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Games',
            fields=[
                ('id', models.CharField(default='a6b4e89e-fd72-413b-b684-9721b053c6e0', max_length=200, primary_key=True, serialize=False)),
                ('ts', models.CharField(default='2020-03-24 21:54:54.657507', max_length=50)),
                ('game_state', models.CharField(default='IN_PROGRESS', max_length=20)),
                ('winner', models.CharField(default='None', max_length=20)),
                ('dimension', models.PositiveIntegerField(default=3)),
            ],
            options={
                'db_table': 'games',
            },
        ),
        migrations.CreateModel(
            name='Moves',
            fields=[
                ('id', models.CharField(default='043bf78b-fae3-4522-ad3a-7cd8e752be75', max_length=200, primary_key=True, serialize=False)),
                ('ts', models.CharField(default='2020-03-24 21:54:54.657998', max_length=50)),
                ('board', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1), blank=True, default=list, size=3), size=3)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tttRL.Games')),
            ],
            options={
                'db_table': 'moves',
            },
        ),
    ]
