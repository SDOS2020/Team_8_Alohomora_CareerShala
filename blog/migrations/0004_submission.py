# Generated by Django 3.1.3 on 2020-12-21 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0003_auto_20201218_0212'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_file', models.FileField(upload_to='student_uploads/')),
                ('uploaded_time', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_submissions',
                                           to='blog.post')),
                ('student_profile',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_submissions',
                                   to=settings.AUTH_USER_MODEL, to_field='identifier')),
            ],
        ),
    ]
