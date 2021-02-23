# Generated by Django 3.1.3 on 2021-02-23 18:32

from django.db import migrations, models
import django.db.models.deletion
import tagulous.models.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                ('count', models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use')),
                ('protected', models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0')),
                ('path', models.TextField()),
                ('label', models.CharField(help_text='The name of the tag, without ancestors', max_length=255)),
                ('level', models.IntegerField(default=1, help_text='The level of the tag in the tree')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='tag.tag')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
                'unique_together': {('slug', 'parent')},
            },
            bases=(tagulous.models.models.BaseTagTreeModel, models.Model),
        ),
    ]