# Generated by Django 4.2.1 on 2023-05-23 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CFO', '0003_alter_coa_superid'),
    ]

    operations = [
        migrations.AddField(
            model_name='coa',
            name='concatenated_id',
            field=models.CharField(default=0, max_length=100, unique=True),
            preserve_default=False,
        ),
    ]