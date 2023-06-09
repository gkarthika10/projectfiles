# Generated by Django 3.2.13 on 2023-03-31 13:38

from django.db import migrations
import salesforce.fields


class Migration(migrations.Migration):

    dependencies = [
        ('opscentre_usermanagement_api', '0013_alter_opsteam_opsrole'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opsteam',
            name='id',
            field=salesforce.fields.CharField(blank=True, db_column='Id__c', max_length=1300, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='opsteamrole',
            name='id',
            field=salesforce.fields.CharField(blank=True, db_column='Id__c', max_length=1300, primary_key=True, serialize=False),
        ),
    ]
