# Generated by Django 3.2.13 on 2023-03-31 12:56

from django.db import migrations
import salesforce.fields


class Migration(migrations.Migration):

    dependencies = [
        ('opscentre_usermanagement_api', '0011_opsrole'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opsteam',
            name='id',
            field=salesforce.fields.SalesforceAutoField(auto_created=True, db_column='Id', primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='opsteamrole',
            name='id',
            field=salesforce.fields.SalesforceAutoField(auto_created=True, db_column='Id', primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]