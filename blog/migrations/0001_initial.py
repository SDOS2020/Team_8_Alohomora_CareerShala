# Generated by Django 3.1.3 on 2020-12-17 19:56

from django.db import migrations, models
import django_bleach.models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('type',
                 models.PositiveSmallIntegerField(choices=[(1, 'Article'), (2, 'Course'), (3, 'Job'), (4, 'Project')],
                                                  default=1)),
                ('title', models.CharField(max_length=255)),
                ('body', django_bleach.models.BleachField()),
                ('preview', models.CharField(help_text='A short preview of this post that is shown in list of posts.',
                                             max_length=300)),
                ('allow_comments', models.BooleanField(default=True)),
            ],
        ),
    ]