# Generated by Django 3.0.4 on 2020-03-25 10:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('localusers', '0004_auto_20200310_1649'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0003_event_server'),
    ]

    operations = [
        migrations.AddField(
            model_name='participation',
            name='notified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='participation',
            name='notify_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='sub_chan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='localusers.DiscoChannel'),
        ),
        migrations.AlterField(
            model_name='game',
            name='sub_users',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
