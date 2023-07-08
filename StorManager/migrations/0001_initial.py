# Generated by Django 4.2.2 on 2023-06-20 09:47

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
            name='Estore',
            fields=[
                ('EstorId', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('EstoreName', models.CharField(max_length=60)),
                ('PhoneNumber', models.CharField(max_length=15)),
                ('EmailAddress', models.CharField(max_length=60)),
                ('Address', models.TextField(blank=True, max_length=100, null=True)),
                ('Type', models.CharField(max_length=60)),
                ('Description', models.TextField(max_length=300)),
                ('ApprovalSataus', models.CharField(default='Pending', max_length=15)),
                ('Status', models.CharField(default='Pending', max_length=15)),
                ('NumberOfItems', models.IntegerField(default=0)),
                ('TsAndCsAccepted', models.BooleanField(default=False)),
                ('CreatDate', models.DateTimeField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('ItemId', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('ItemName', models.CharField(max_length=60)),
                ('Price', models.CharField(max_length=22)),
                ('BuyPrice', models.CharField(max_length=22)),
                ('Profit', models.CharField(default='0', max_length=70)),
                ('Investament', models.CharField(max_length=70)),
                ('NumSold', models.IntegerField()),
                ('Quantity', models.IntegerField()),
                ('Status', models.CharField(default='Available', max_length=15)),
                ('ExpDate', models.DateTimeField()),
                ('ItemVisual', models.CharField(max_length=300)),
                ('AddeBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('EstorId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='StorManager.estore')),
            ],
        ),
        migrations.CreateModel(
            name='Finance',
            fields=[
                ('FinanceId', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('TotalItemsSold', models.IntegerField()),
                ('EstoreProfit', models.CharField(max_length=22)),
                ('TotalInvestment', models.CharField(max_length=22)),
                ('EstorId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='StorManager.estore')),
            ],
        ),
    ]
