# Generated by Django 4.1.5 on 2023-02-03 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0017_profile_first_name_profile_last_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Base.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Base.profile')),
            ],
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]