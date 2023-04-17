# Generated by Django 3.2.13 on 2023-03-31 22:25

from django.db import migrations
import django.db.models.deletion
import salesforce.fields


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement_api', '0003_candidateprofile_cand_id'),
        ('opscentre_usermanagement_api', '0019_alter_servicerq_recruiter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicerq',
            name='recruiter',
            field=salesforce.fields.ForeignKey(blank=True, db_column='Recruiter__c', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='usermanagement_api.contact', verbose_name='Contact'),
        ),
    ]