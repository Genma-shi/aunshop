# Generated by Django 4.2.23 on 2025-07-06 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stationery', '0002_alter_category_options_alter_stationery_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stationery',
            name='images',
        ),
        migrations.AddField(
            model_name='stationeryimage',
            name='stationery',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='stationery.stationery', verbose_name='Товар'),
            preserve_default=False,
        ),
    ]
