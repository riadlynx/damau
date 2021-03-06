# Generated by Django 2.0.1 on 2018-05-12 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('up', '0003_rapport'),
    ]

    operations = [
        migrations.AddField(
            model_name='barrage',
            name='BV',
            field=models.CharField(default='Bassin versant', max_length=100),
        ),
        migrations.AddField(
            model_name='barrage',
            name='CP',
            field=models.CharField(default='Crue de projet', max_length=100),
        ),
        migrations.AddField(
            model_name='barrage',
            name='O',
            field=models.CharField(default='oued', max_length=100),
        ),
        migrations.AddField(
            model_name='barrage',
            name='P',
            field=models.CharField(default='province', max_length=100),
        ),
        migrations.AddField(
            model_name='barrage',
            name='PHE',
            field=models.CharField(default='PHE', max_length=100),
        ),
        migrations.AddField(
            model_name='barrage',
            name='RN',
            field=models.CharField(default='RN', max_length=100),
        ),
        migrations.AddField(
            model_name='barrage',
            name='T',
            field=models.CharField(default='type de barrages', max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='company',
            field=models.CharField(default='company', max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='tel',
            field=models.CharField(default='tel', max_length=100),
        ),
    ]
