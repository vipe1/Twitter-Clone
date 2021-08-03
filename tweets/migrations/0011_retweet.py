# Generated by Django 3.2.4 on 2021-07-31 16:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tweets', '0010_alter_comment_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Retweet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='retweets', to=settings.AUTH_USER_MODEL)),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='retweets', to='tweets.tweet')),
            ],
        ),
    ]
