# Generated by Django 4.2.2 on 2023-06-20 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StorManager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='ItemDescription',
            field=models.TextField(default='Describe', max_length=300),
        ),
        migrations.AlterField(
            model_name='item',
            name='ExpDate',
            field=models.CharField(default='Not applicable', max_length=60),
        ),
    ]
