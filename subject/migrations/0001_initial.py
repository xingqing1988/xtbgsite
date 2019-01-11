# Generated by Django 2.0 on 2018-10-12 02:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='uploads/file/%Y/%m/%d/')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='uploads/image/%Y/%m/%d/')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('content', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
        migrations.CreateModel(
            name='SubjectLevelOne',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectLevelTwo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=20)),
                ('level_two_for_one', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='subject.SubjectLevelOne')),
            ],
        ),
        migrations.CreateModel(
            name='SubjectType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='SupFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/supfile/%Y/%m/%d/')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
        migrations.CreateModel(
            name='SupFileType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='supfile',
            name='file_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='subject.SupFileType'),
        ),
        migrations.AddField(
            model_name='subject',
            name='subject_level_one',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='subject.SubjectLevelOne'),
        ),
        migrations.AddField(
            model_name='subject',
            name='subject_level_two',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='subject.SubjectLevelTwo'),
        ),
        migrations.AddField(
            model_name='subject',
            name='subject_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='subject.SubjectType'),
        ),
        migrations.AddField(
            model_name='image',
            name='image_sub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='subject.Subject'),
        ),
        migrations.AddField(
            model_name='file',
            name='file_sub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='subject.Subject'),
        ),
    ]