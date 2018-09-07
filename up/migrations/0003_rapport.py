# Generated by Django 2.0.1 on 2018-03-03 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('up', '0002_auto_20180218_2119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rapport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('fich', models.FileField(upload_to='')),
                ('prof', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='up.Profile')),
            ],
        ),
    ]