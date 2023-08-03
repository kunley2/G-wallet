# Generated by Django 4.2.2 on 2023-07-30 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salte', '0002_account_account_name_account_account_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='first_name',
            field=models.CharField(default='tonks', max_length=250, verbose_name='First name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='last_name',
            field=models.CharField(default='dex', max_length=250, verbose_name='Last name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='passcode',
            field=models.IntegerField(verbose_name='pass_code'),
        ),
    ]
