# Generated by Django 4.1.5 on 2023-01-31 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0004_alter_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
