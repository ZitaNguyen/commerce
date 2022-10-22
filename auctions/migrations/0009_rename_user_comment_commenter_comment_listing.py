# Generated by Django 4.1.1 on 2022-10-22 19:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_rename_user_bid_bidder'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='commenter',
        ),
        migrations.AddField(
            model_name='comment',
            name='listing',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='listing_commented', to='auctions.listing'),
            preserve_default=False,
        ),
    ]
