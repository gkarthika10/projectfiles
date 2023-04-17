# Generated by Django 3.2.13 on 2023-04-09 11:31

from django.db import migrations
import salesforce.fields


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement_api', '0003_candidateprofile_cand_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='created_date',
            field=salesforce.fields.DateTimeField(db_column='CreatedDate', null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='created_date',
            field=salesforce.fields.DateTimeField(db_column='CreatedDate', null=True),
        ),
    ]