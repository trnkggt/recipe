# Generated by Django 4.1.5 on 2023-01-31 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0002_delete_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(null=True, upload_to='Base/static/images'),
        ),
    ]
