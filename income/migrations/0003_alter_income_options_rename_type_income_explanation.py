# Generated by Django 4.1.5 on 2023-02-12 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('income', '0002_alter_income_price_alter_income_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='income',
            options={'verbose_name_plural': 'هزینه کردها'},
        ),
        migrations.RenameField(
            model_name='income',
            old_name='type',
            new_name='explanation',
        ),
    ]
