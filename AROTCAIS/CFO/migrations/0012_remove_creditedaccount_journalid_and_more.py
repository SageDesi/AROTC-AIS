# Generated by Django 4.0.2 on 2023-05-26 04:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CFO', '0011_creditedaccount_coa_id_debitedaccount_coa_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditedaccount',
            name='JournalID',
        ),
        migrations.RemoveField(
            model_name='debitedaccount',
            name='JournalID',
        ),
    ]