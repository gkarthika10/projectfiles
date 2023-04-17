from salesforce import models
from usermanagement_api.models import *

# Create your models here.


class OpsRole(models.Model):
    name = models.CharField(db_column='Name', unique=True, max_length=80)
    #id = models.CharField(db_column='Id__c', max_length=1300, sf_read_only=models.READ_ONLY, blank= True,primary_key=True)
    record_id = models.CharField(db_column='RoleId__c', max_length=1300, sf_read_only=models.READ_ONLY, blank= True)
    class Meta(models.Model.Meta):
        db_table = 'OpsRole__c'
        verbose_name = 'OpsRole'
        verbose_name_plural = 'OpsRoles'


class OpsTeamRole(models.Model):
    name = models.CharField(db_column='Name', unique=True, max_length=80)
    record_id = models.CharField(db_column='Id__c', max_length=1300, sf_read_only=models.READ_ONLY, blank= True)
    role_id = models.CharField(db_column='RoleId__c', max_length=1300, sf_read_only=models.READ_ONLY, blank= True)
    class Meta(models.Model.Meta):
        db_table = 'OpsTeamRole__c'
        verbose_name = 'OpsTeamRole'
        verbose_name_plural = 'OpsTeamRoles'

class OpsTeam(models.Model):
    created_date = models.DateTimeField(db_column='CreatedDate', sf_read_only=models.READ_ONLY)
    email = models.EmailField(db_column='Name', unique=True)
    password = models.CharField(db_column='Password__c', max_length=255)
    first_name = models.CharField(db_column='first_name__c', max_length=255, default=models.DefaultedOnCreate(False))
    last_name = models.CharField(db_column='last_name__c', max_length=255, default= models.DefaultedOnCreate(False))
    #OpsRole = models.CharField(db_column='OpsRole__c', max_length=255, default=models.DefaultedOnCreate('User'), choices=[('Admin', 'Admin'), ('User', 'User')])
    OpsRole = models.ForeignKey('OpsTeamRole', models.DO_NOTHING, db_column='OpsTeamRole__c', verbose_name='OpsTeamRole')
    active = models.BooleanField(db_column='Active__c', default=models.DefaultedOnCreate(False))
    approved = models.BooleanField(db_column='Approved__c', default=models.DefaultedOnCreate(False))
    ops_id = models.CharField(db_column='TeamId__c', max_length=1300, sf_read_only=models.READ_ONLY, blank=True)
    record_id = models.CharField(db_column='Id__c', max_length=1300, sf_read_only=models.READ_ONLY, blank=True)
    roleName = models.CharField(db_column='RoleName__c', max_length=1300, sf_read_only=models.READ_ONLY, blank=True)
    class Meta(models.Model.Meta):
        db_table = 'OpsTeam__c'
        verbose_name = 'OpsTeam'
        verbose_name_plural = 'OpsTeams'




class ServiceRq(models.Model):
    opsteam = models.ForeignKey('OpsTeam',models.DO_NOTHING,db_column='OpsTeam__c',blank=True, null=True)
    auction = models.ForeignKey('auction_api.Auction', models.DO_NOTHING, db_column='Auction__c',blank=True, null=True)
    candidate = models.ForeignKey('usermanagement_api.Candidate', models.DO_NOTHING, db_column='Candidate__c',blank=True, null=True)
    #created_by = models.ForeignKey('User', models.DO_NOTHING, db_column = 'CreatedById')
    create_time_stamp = models.DateTimeField(db_column='createTimeStamp__c',sf_read_only=models.READ_ONLY)
    detailed_notes = models.TextField(db_column='DetailedNotes__c', blank=True, null=True)
    #last_modified_by = models.ForeignKey('User', models.DO_NOTHING, db_column = 'LastModifiedById')
    #owner = models.ForeignKey('Group', models.DO_NOTHING, db_column='OwnerId', verbose_name='Owner ID', default=models.DEFAULTED_ON_CREATE)
    priority = models.CharField(db_column='Priority__c', max_length=255, verbose_name='Priority', choices=[('Urgent', 'Urgent'), ('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], blank=True, null=True)
    recruiter = models.ForeignKey('usermanagement_api.Contact', models.DO_NOTHING, db_column='Recruiter__c', verbose_name='Contact',blank=True, null=True) 
   #rq_id = models.AutoField(db_column='Name',primary_key=True)
    short_desc = models.CharField(db_column='ShortDesc__c',max_length=255,blank=True, null=True)
    rq_id = models.CharField(db_column='Name', max_length=1300, sf_read_only=models.READ_ONLY, blank=True)
    record_id = models.CharField(db_column='Id__c', max_length=1300, sf_read_only=models.READ_ONLY, blank=True)
    cand_id = models.CharField(db_column='cand_id__c', max_length=1300, sf_read_only=models.READ_ONLY, blank=True)
    auc_id = models.CharField(db_column='auc_Id__c', max_length=1300, sf_read_only=models.READ_ONLY, blank=True)
    ops_id = models.CharField(db_column='Ops_id__c', max_length=1300, sf_read_only=models.READ_ONLY, blank=True)
    rec_id = models.CharField(db_column='rec_id__c', max_length=1300, sf_read_only=models.READ_ONLY, blank=True)
    create_dtime = models.DateTimeField(db_column='createDt__c',sf_read_only=models.READ_ONLY,blank=True,null = True)
    status = models.CharField(db_column='Status__c',max_length=255, verbose_name='Status',choices=[('Open','Open'),('In-Progress','In-Progress'),('Closed','Closed')])
    update_time_stamp = models.DateTimeField(db_column='updateTimeStamp__c',sf_read_only=models.READ_ONLY)
    class Meta(models.Model.Meta):
        db_table = 'ServiceRq__c'
        verbose_name = 'ServiceRq'
        verbose_name_plural = 'ServiceRqs'

class SR_comments(models.Model):
    candidate = models.ForeignKey('usermanagement_api.Candidate', models.DO_NOTHING, db_column='Candidate__c', blank=True, null=True)
    #cmnt_id = models.AutoField(db_column='Name',primary_key=True)
    comment = models.TextField(db_column='Comment__c', blank=True, null=True)
    #created_by = models.ForeignKey('User', models.DO_NOTHING, db_column = 'CreatedById')
    #last_modified_by = models.ForeignKey('User', models.DO_NOTHING, db_column = 'LastModifiedById')
    ops_user = models.ForeignKey(OpsTeam, models.DO_NOTHING, db_column='OpsTeam__c', blank=True, null=True)
    record_id = models.CharField(db_column='Id__c', max_length=1300, sf_read_only=models.READ_ONLY, blank=True)
    #owner = models.ForeignKey('Group', models.DO_NOTHING, db_column='OwnerId', verbose_name='Owner ID', default=models.DEFAULTED_ON_CREATE)
    recruiter = models.ForeignKey('usermanagement_api.Contact', models.DO_NOTHING, db_column='Recruiter__c', verbose_name='Contact ID', blank=True, null=True) 
    service_rq = models.ForeignKey('ServiceRq', models.DO_NOTHING, db_column='ServiceRq__c', blank=True, null=True)
    srq_id = models.DateTimeField(db_column='SRQ_Id__c',sf_read_only=models.READ_ONLY),
    dtime = models.DateTimeField(db_column='TimeStamp__c',blank=True, null = True),
    create_dtime = models.DateTimeField(db_column='createDt__c',sf_read_only=models.READ_ONLY,blank=True,null = True)
    class Meta(models.Model.Meta):
        db_table = 'SR_comments__c'
        verbose_name = 'Srcomments'
        verbose_name_plural = 'Srcomments'


class DashboardCache(models.Model):
    name = models.CharField(db_column='Name',max_length=80)
    count = models.IntegerField(db_column='Count__c')
    record_id = models.CharField(db_column='Id__c', max_length=1300, sf_read_only=models.READ_ONLY, blank=True)
    create_dtime = models.DateTimeField(db_column='createDt__c',sf_read_only=models.READ_ONLY,blank=True,null = True)
    class Meta(models.Model.Meta):
        db_table = 'DashboardCache__c'
        verbose_name = 'DashboardCache'
        verbose_name_plural = 'DashboardCache'

class SchedulerInterval(models.Model):
    name = models.CharField(db_column='Name',max_length=80)
    interval = models.IntegerField(db_column='Interval__c')
    record_id = models.CharField(db_column='Id__c', max_length=1300, sf_read_only=models.READ_ONLY, blank=True)
    create_dtime = models.DateTimeField(db_column='createDt__c',sf_read_only=models.READ_ONLY,blank=True,null = True)
    class Meta(models.Model.Meta):
        db_table = 'SchedulerInterval__c'
        verbose_name = 'SchedulerInterval'
        verbose_name_plural = 'SchedulerInterval'
