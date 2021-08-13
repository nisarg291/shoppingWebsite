# Generated by Django 3.1.1 on 2021-08-12 07:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20210812_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='paytmhistory',
            name='address',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='shop.useraddress1'),
        ),
        migrations.AlterField(
            model_name='paytmhistory',
            name='checout',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='shop.checkout'),
        ),
    ]