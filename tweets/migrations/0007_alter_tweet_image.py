# Generated by Django 3.2.4 on 2021-07-13 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0006_rename_media_tweet_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
