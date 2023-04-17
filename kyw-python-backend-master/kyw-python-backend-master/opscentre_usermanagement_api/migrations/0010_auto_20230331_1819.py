# Generated by Django 3.2.13 on 2023-03-31 12:49

from django.db import migrations
import django.db.models.deletion
import django.db.models.manager
import salesforce.fields


class Migration(migrations.Migration):

    dependencies = [
        ('opscentre_usermanagement_api', '0009_auto_20230331_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpsTeamRole',
            fields=[
                ('name', salesforce.fields.CharField(db_column='Name', max_length=80, unique=True)),
                ('id', salesforce.fields.CharField(blank=True, db_column='Id__c', max_length=1300, primary_key=True, serialize=False)),
                ('record_id', salesforce.fields.CharField(blank=True, db_column='RoleId__c', max_length=1300)),
            ],
            options={
                'verbose_name': 'OpsTeamRole',
                'verbose_name_plural': 'OpsTeamRoles',
                'db_table': 'OpsTeamRole__c',
                'abstract': False,
                'base_manager_name': 'base_manager',
            },
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='opsteam',
            name='id',
            field=salesforce.fields.CharField(blank=True, db_column='Id__c', max_length=1300, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='opsteam',
            name='record_id',
            field=salesforce.fields.CharField(blank=True, db_column='TeamId__c', max_length=1300),
        ),
        migrations.AlterField(
            model_name='opsteam',
            name='OpsRole',
            field=salesforce.fields.ForeignKey(db_column='OpsRole__c', on_delete=django.db.models.deletion.DO_NOTHING, to='opscentre_usermanagement_api.opsteamrole'),
        ),
        migrations.DeleteModel(
            name='OpsRole',
        ),
    ]