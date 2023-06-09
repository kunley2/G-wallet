# Generated by Django 4.2.2 on 2023-07-11 10:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('photo', models.ImageField(upload_to='images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Account',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('funding', 'Bank Transfer Funding'), ('payout', 'Bank Transfer Payout'), ('debit user wallet', 'Debit User Wallet'), ('credit user wallet', 'Credit User Wallet')], max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=100, verbose_name='amount')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('success', 'Success'), ('fail', 'Fail')], default='pending', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='salte.account')),
            ],
            options={
                'db_table': 'Transaction',
                'managed': True,
            },
        ),
    ]
