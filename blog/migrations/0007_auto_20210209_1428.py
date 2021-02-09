# Generated by Django 3.1.3 on 2021-02-09 08:58

from django.db import migrations
import tagulous.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0001_initial'),
        ('blog', '0006_auto_20210203_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=tagulous.models.fields.TagField(_set_tag_meta=True, blank=True, force_lowercase=True, help_text='Enter a comma-separated tag string', related_name='posts', to='tag.Tag', tree=True),
        ),
    ]
