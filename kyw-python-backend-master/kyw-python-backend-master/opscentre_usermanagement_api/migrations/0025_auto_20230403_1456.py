# Generated by Django 3.2.13 on 2023-04-03 09:26

from django.db import migrations
import django.db.models.deletion
import salesforce.fields


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement_api', '0003_candidateprofile_cand_id'),
        ('opscentre_usermanagement_api', '0024_auto_20230403_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sr_comments',
            name='candidate',
            field=salesforce.fields.ForeignKey(blank=True, db_column='Candidate__c', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='usermanagement_api.candidate'),
        ),
        migrations.AlterField(
            model_name='sr_comments',
            name='ops_user',
            field=salesforce.fields.ForeignKey(blank=True, db_column='OpsTeam__c', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='opscentre_usermanagement_api.opsteam'),
        ),
        migrations.AlterField(
            model_name='sr_comments',
            name='recruiter',
            field=salesforce.fields.ForeignKey(blank=True, db_column='Recruiter__c', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='usermanagement_api.contact', verbose_name='Contact ID'),
        ),
    ]
