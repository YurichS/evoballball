# Generated by Django 4.2.7 on 2023-11-05 21:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EBBApp', '0002_alter_product_image'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='product',
            index_together={('id', 'slug')},
        ),
    ]
