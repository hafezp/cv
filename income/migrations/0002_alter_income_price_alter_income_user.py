# Generated by Django 4.1.5 on 2023-02-12 16:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('income', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='price',
            field=models.DecimalField(decimal_places=0, default=45500, help_text='تومان', max_digits=10, verbose_name='مبلغ ریالی'),
        ),
        migrations.AlterField(
            model_name='income',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
