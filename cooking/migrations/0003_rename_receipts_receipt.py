# Generated by Django 4.1.1 on 2022-10-04 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cooking', '0002_receiptrating'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Receipts',
            new_name='Receipt',
        ),
    ]
