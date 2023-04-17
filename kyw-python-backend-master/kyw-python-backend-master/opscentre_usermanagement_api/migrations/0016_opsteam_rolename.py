# Generated by Django 3.2.13 on 2023-03-31 14:48

from django.db import migrations
import salesforce.fields


class Migration(migrations.Migration):

    dependencies = [
        ('opscentre_usermanagement_api', '0015_alter_opsteam_opsrole'),
    ]

    operations = [
        migrations.AddField(
            model_name='opsteam',
            name='roleName',
            field=salesforce.fields.CharField(blank=True, db_column='RoleName__c', max_length=1300),
        ),
    ]
