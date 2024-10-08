# Generated by Django 4.2.14 on 2024-08-07 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_remove_recipe_categories_recipe_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='category',
            field=models.CharField(choices=[('appetisers/snacks', 'Appetizers/Snacks'), ('beverages', 'Beverages'), ('soups', 'Soups'), ('salads', 'Salads'), ('vegan', 'Vegan'), ('vegeterian', 'Vegeterian'), ('main dishes', 'Main Dishes'), ('desserts', 'Desserts')], default='main dishes', max_length=50),
        ),
    ]
