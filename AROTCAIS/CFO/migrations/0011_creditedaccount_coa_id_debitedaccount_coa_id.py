# Generated by Django 4.0.2 on 2023-05-26 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CFO', '0010_creditedaccount_debitedaccount_delete_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditedaccount',
            name='COA_ID',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='debitedaccount',
            name='COA_ID',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
