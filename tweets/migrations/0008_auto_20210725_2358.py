# Generated by Django 3.2.4 on 2021-07-25 21:58

from django.db import migrations, models
import tweets.models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0007_alter_tweet_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='update_date',
        ),
        migrations.AlterField(
            model_name='tweet',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=tweets.models.get_upload_path),
        ),
    ]
