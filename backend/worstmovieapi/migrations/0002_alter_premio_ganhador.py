# Generated by Django 5.2 on 2025-04-03 02:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worstmovieapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='premio',
            name='ganhador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ganhador', to='worstmovieapi.filme'),
        ),
    ]
