# Generated by Django 4.1.1 on 2022-10-12 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_listing_bids_alter_listing_comments_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(upload_to='images'),
        ),
    ]
