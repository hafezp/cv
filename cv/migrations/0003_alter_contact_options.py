# Generated by Django 4.1.5 on 2023-02-12 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cv', '0002_alter_ipaddress_pub_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ['-publish'], 'verbose_name': 'پیام', 'verbose_name_plural': 'پیام ها'},
        ),
    ]