# Generated by Django 4.2.7 on 2023-11-29 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=150)),
                ('full_names', models.CharField(max_length=150)),
                ('subject', models.CharField(max_length=400)),
                ('message', models.TextField()),
            ],
        ),
    ]
