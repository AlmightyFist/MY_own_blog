# Generated by Django 2.0.6 on 2018-07-05 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20180705_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='avr_score',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3, null=True),
        ),
    ]