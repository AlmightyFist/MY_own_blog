# Generated by Django 2.0.6 on 2018-07-10 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20180705_1544'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CategoryName', models.CharField(max_length=250)),
                ('Post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post')),
            ],
        ),
    ]
