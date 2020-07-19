# Generated by Django 2.2.12 on 2020-07-19 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ilend', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='offlinewallet',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_id_offlinewallet', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lenders',
            name='lender',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='lender_user_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lcards',
            name='lender',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='lender_user_id_lcards', to='ilend.lenders'),
        ),
    ]
