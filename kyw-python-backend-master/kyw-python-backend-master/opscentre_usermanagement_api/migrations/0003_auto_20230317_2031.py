# Generated by Django 3.2.13 on 2023-03-17 15:01

from django.db import migrations
import django.db.models.manager
import salesforce.fields


class Migration(migrations.Migration):

    dependencies = [
        ('opscentre_usermanagement_api', '0002_auto_20230317_1646')
    ]

    operations = [
        migrations.CreateModel(
            name='OpsTeam',
            fields=[
                ('id', salesforce.fields.SalesforceAutoField(auto_created=True, db_column='Id', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', salesforce.fields.DateTimeField(db_column='CreatedDate')),
                ('email', salesforce.fields.EmailField(db_column='Name', max_length=254, unique=True)),
                ('password', salesforce.fields.CharField(db_column='Password__c', max_length=255)),
                ('OpsRole', salesforce.fields.CharField(choices=[('SuperAdmin', 'SuperAdmin'), ('Admin', 'Admin'), ('User', 'User')], db_column='OpsRole__c', default=salesforce.fields.DefaultedOnCreate('User'), max_length=255)),
                ('active', salesforce.fields.BooleanField(db_column='Active__c', default=salesforce.fields.DefaultedOnCreate())),
                ('approved', salesforce.fields.BooleanField(db_column='Approved__c', default=salesforce.fields.DefaultedOnCreate())),
                ('record_id', salesforce.fields.CharField(blank=True, db_column='Id__c', max_length=1300)),
            ],
            options={
                'db_table': 'OpsTeam__c',
                'abstract': False,
                'base_manager_name': 'base_manager',
            },
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
