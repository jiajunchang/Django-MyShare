# Generated by Django 3.0.2 on 2020-02-21 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0007_image_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='url',
            field=models.URLField(null=True),
        ),
    ]
