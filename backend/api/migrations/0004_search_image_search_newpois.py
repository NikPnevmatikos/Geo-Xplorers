# Generated by Django 4.2.1 on 2023-07-04 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_announcement_id_announcement__id'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='image',
            field=models.ImageField(blank=True, default='/defaultMap.png', null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='search',
            name='newPois',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
