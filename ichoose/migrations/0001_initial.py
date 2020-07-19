# Generated by Django 2.2.12 on 2020-07-19 14:45

from django.db import migrations, models
import djongo.models.fields
import ichoose.list_field
import ichoose.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='buyers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_list', djongo.models.fields.ArrayField(default=[], model_container=ichoose.models.order_abs, model_form_class=ichoose.models.order_abs_form)),
                ('ratings_comments', djongo.models.fields.ArrayField(default=[], model_container=ichoose.models.ratings_comments_abs, model_form_class=ichoose.models.ratings_comments_abs_form)),
                ('customization_requests_list', djongo.models.fields.ArrayField(default=[], model_container=ichoose.models.customization_abs, model_form_class=ichoose.models.customization_abs_form)),
            ],
        ),
        migrations.CreateModel(
            name='customization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField()),
                ('customization_details', ichoose.list_field.CustomListField(default=[])),
                ('request_status', models.BooleanField(default=False)),
                ('accepted_details', ichoose.list_field.CustomListField(default=[])),
                ('accept_status', models.BooleanField(default=False)),
                ('reject_status', models.BooleanField(default=False)),
                ('order_id', models.IntegerField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='loan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_applied_date', models.DateTimeField()),
                ('loan_status', models.BooleanField(default=False)),
                ('loan_amount', models.IntegerField(default=None)),
                ('loan_intrest', models.IntegerField()),
                ('loan_returned_status', models.BooleanField(default=False)),
                ('loan_returned_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_order', models.DateTimeField()),
                ('told_date_of_order', models.DateTimeField()),
                ('date_of_delivery', models.DateTimeField()),
                ('order_details', djongo.models.fields.EmbeddedField(model_container=ichoose.models.order_details_abs, model_form_class=ichoose.models.order_details_abs_form, null=True)),
                ('quantity', models.IntegerField()),
                ('total_price', models.TextField()),
                ('payment_status', models.BooleanField(default=False)),
                ('delivery_status', models.BooleanField(default=False)),
                ('loan_status', models.BooleanField(default=False)),
                ('loan_amount', models.IntegerField(default=None)),
                ('cancel_status', models.BooleanField(default=False)),
                ('cancel_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_post', models.DateTimeField()),
                ('product_title', models.TextField()),
                ('category_1', models.TextField()),
                ('category_2', models.TextField()),
                ('product_description', models.TextField()),
                ('product_name', models.TextField()),
                ('product_detail', models.TextField()),
                ('product_color', ichoose.list_field.CustomListField(default=[])),
                ('product_size', models.TextField()),
                ('product_price', models.FloatField()),
                ('product_discount', models.FloatField()),
                ('product_final_price', models.FloatField()),
                ('product_remaining_details', ichoose.list_field.CustomListField(default=[])),
                ('additional_information', models.TextField()),
                ('images', ichoose.list_field.CustomListField(default=[])),
                ('product_customisation_available', ichoose.list_field.CustomListField(default=[])),
                ('additional_customization_information', models.TextField()),
                ('order_list', djongo.models.fields.ArrayField(default=[], model_container=ichoose.models.order_abs, model_form_class=ichoose.models.order_abs_form)),
                ('ratings_comments', djongo.models.fields.ArrayField(default=[], model_container=ichoose.models.ratings_comments_abs, model_form_class=ichoose.models.ratings_comments_abs_form)),
                ('customization_requests_list', djongo.models.fields.ArrayField(default=[], model_container=ichoose.models.customization_abs, model_form_class=ichoose.models.customization_abs_form)),
            ],
        ),
        migrations.CreateModel(
            name='ratings_comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=255)),
                ('date_time', models.DateTimeField()),
                ('verified_user', models.BooleanField(default=False)),
                ('like', models.BooleanField(default=False)),
                ('comment', models.TextField()),
                ('rating', models.IntegerField()),
                ('reply', models.TextField()),
                ('reply_timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='seller_verification_process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=50)),
                ('address_line_1', models.CharField(max_length=100)),
                ('address_line_2', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=50)),
                ('purpose', models.TextField()),
                ('images', djongo.models.fields.ListField(default=[])),
                ('files', djongo.models.fields.ListField(default=[])),
                ('Verification_step_1', models.BooleanField(default=False)),
                ('Verification_step_2', models.BooleanField(default=False)),
                ('Verification_step_3', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='sellers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_list', djongo.models.fields.ArrayField(default=[], model_container=ichoose.models.product_abs, model_form_class=ichoose.models.product_abs_form)),
                ('order_list', djongo.models.fields.ArrayField(default=[], model_container=ichoose.models.order_abs, model_form_class=ichoose.models.order_abs_form)),
                ('loan_list', djongo.models.fields.ArrayField(default=[], model_container=ichoose.models.loan_abs, model_form_class=ichoose.models.loan_abs_form)),
                ('customization_requests_list', djongo.models.fields.ArrayField(default=[], model_container=ichoose.models.customization_abs, model_form_class=ichoose.models.customization_abs_form)),
            ],
        ),
    ]
