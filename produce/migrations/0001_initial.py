# Generated by Django 5.1.6 on 2025-02-26 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('demand', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], max_length=50)),
                ('type', models.CharField(choices=[('vegetable', 'Vegetable'), ('fruit', 'Fruit'), ('grain', 'Grain'), ('dairy', 'Dairy'), ('meat', 'Meat'), ('other', 'Other')], max_length=50)),
                ('check_frequency', models.CharField(max_length=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to='produce_images/')),
            ],
        ),
    ]
