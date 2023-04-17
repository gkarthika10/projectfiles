from salesforce import models

class Candidate(models.Model):
    # owner = models.ForeignKey('Group', models.DO_NOTHING, db_column='OwnerId', verbose_name='Owner ID', default=models.DEFAULTED_ON_CREATE)  # Reference to tables [Group, User]
    # is_deleted = models.BooleanField(db_column='IsDeleted', verbose_name='Deleted', sf_read_only=models.READ_ONLY, default=False)
    #name = models.CharField(db_column='Name', max_length=80, verbose_name='Candidate  Name', default=models.DEFAULTED_ON_CREATE, blank=True, null=True)
    created_date = models.DateTimeField(db_column='CreatedDate', sf_read_only=models.READ_ONLY)
    # created_by = models.ForeignKey('User', models.DO_NOTHING, db_column='CreatedById', related_name='candidate_createdby_set', verbose_name='Created By ID', sf_read_only=models.READ_ONLY)
    # last_modified_date = models.DateTimeField(db_column='LastModifiedDate', sf_read_only=models.READ_ONLY)
    # last_modified_by = models.ForeignKey('User', models.DO_NOTHING, db_column='LastModifiedById', related_name='candidate_lastmodifiedby_set', verbose_name='Last Modified By ID', sf_read_only=models.READ_ONLY)
    # system_modstamp = models.DateTimeField(db_column='SystemModstamp', sf_read_only=models.READ_ONLY)
    # last_activity_date = models.DateField(db_column='LastActivityDate', sf_read_only=models.READ_ONLY, blank=True, null=True)
    # last_viewed_date = models.DateTimeField(db_column='LastViewedDate', sf_read_only=models.READ_ONLY, blank=True, null=True)
    # last_referenced_date = models.DateTimeField(db_column='LastReferencedDate', sf_read_only=models.READ_ONLY, blank=True, null=True)
    first_name = models.CharField(db_column='First_Name__c', max_length=255, verbose_name='First Name')
    last_name = models.CharField(db_column='Last_Name__c', max_length=255, verbose_name='Last Name', blank=True, null=True)
    phone = models.CharField(db_column='Phone__c', max_length=40)
    email = models.EmailField(db_column='Email__c', unique=True)
    password = models.CharField(db_column='Password__c', max_length=255)
    email_verification = models.BooleanField(db_column='Email_Verification__c', verbose_name='Email Verification', default=models.DefaultedOnCreate(False))
    screening_stages = models.CharField(db_column='Screening_Stages__c', max_length=255, verbose_name='Screening Stages', default=models.DefaultedOnCreate('Draft'), choices=[('Draft', 'Draft'), ('Email Verified', 'Email Verified'), ('Profile Created', 'Profile Created')], blank=True, null=True)
    record_id = models.CharField(db_column='Id__c', max_length=1300, sf_read_only=models.READ_ONLY, blank=True)
    class Meta(models.Model.Meta):
        db_table = 'Candidate__c'
        verbose_name = 'Candidate'
        verbose_name_plural = 'Candidates'
        # keyPrefix = 'a02'

class CandidateProfile(models.Model):
    # owner = models.ForeignKey('Group', models.DO_NOTHING, db_column='OwnerId', verbose_name='Owner ID', default=models.DEFAULTED_ON_CREATE)  # Reference to tables [Group, User]
    # is_deleted = models.BooleanField(db_column='IsDeleted', verbose_name='Deleted', sf_read_only=models.READ_ONLY, default=False)
    # name = models.CharField(db_column='Name', max_length=80, verbose_name='Candidate Profile', sf_read_only=models.READ_ONLY)
    # created_date = models.DateTimeField(db_column='CreatedDate', sf_read_only=models.READ_ONLY)
    # created_by = models.ForeignKey('User', models.DO_NOTHING, db_column='CreatedById', related_name='candidateprofile_createdby_set', verbose_name='Created By ID', sf_read_only=models.READ_ONLY)
    # last_modified_date = models.DateTimeField(db_column='LastModifiedDate', sf_read_only=models.READ_ONLY)
    # last_modified_by = models.ForeignKey('User', models.DO_NOTHING, db_column='LastModifiedById', related_name='candidateprofile_lastmodifiedby_set', verbose_name='Last Modified By ID', sf_read_only=models.READ_ONLY)
    # system_modstamp = models.DateTimeField(db_column='SystemModstamp', sf_read_only=models.READ_ONLY)
    # last_viewed_date = models.DateTimeField(db_column='LastViewedDate', sf_read_only=models.READ_ONLY, blank=True, null=True)
    # last_referenced_date = models.DateTimeField(db_column='LastReferencedDate', sf_read_only=models.READ_ONLY, blank=True, null=True)
    #count_of_profiles = models.DecimalField(db_column='Count_of_Profiles__c', max_digits=18, decimal_places=0, verbose_name='Count of Profiles', default=models.DEFAULTED_ON_CREATE, blank=True, null=True)
    gender = models.CharField(db_column='Gender__c', max_length=255, choices=[('Male', 'Male'), ('Female', 'Female'), ('Not Disclosed', 'Not Disclosed')], blank=True, null=True)
    current_employer = models.CharField(db_column='Current_Employer__c', max_length=200, verbose_name='Current Employer', blank=True, null=True)
    #current_company = models.CharField(db_column='Current_Employer__c', max_length=200, verbose_name='Current Employer', blank=True, null=True)
    cand_id = models.CharField(db_column='cand_id__c', max_length=255, verbose_name='cand_id', blank=True, null=True)
    current_ctc = models.CharField(db_column='Current_CTC__c', max_length=255, verbose_name='Current CTC', blank=True, null=True)
    candidate_email = models.CharField(db_column='Candidate_Email__c', max_length=1300, verbose_name='Candidate Email', sf_read_only=models.READ_ONLY, blank=True, null=True)
    candidate = models.ForeignKey('Candidate', models.DO_NOTHING, db_column='Candidate__c', blank=True, null=True)
    first_name = models.CharField(db_column='First_Name__c', max_length=1300, verbose_name='First Name', sf_read_only=models.READ_ONLY, blank=True, null=True)
    last_name = models.CharField(db_column='Last_Name__c', max_length=1300, verbose_name='Last Name', sf_read_only=models.READ_ONLY, blank=True, null=True)
    # n = models.DecimalField(db_column='n__c', max_digits=18, decimal_places=0, verbose_name='No.of Auctions', default=models.DEFAULTED_ON_CREATE, blank=True, null=True)
    resume_url = models.CharField(db_column='Resume_URL__c', max_length=255, verbose_name='Resume URL', blank=True, null=True)
    about = models.TextField(db_column='About__c', blank=True, null=True)
    experience = models.TextField(db_column='Experience__c', blank=True, null=True)
    projects = models.TextField(db_column='Projects__c', blank=True, null=True)
    certifications = models.TextField(db_column='Certifications__c', blank=True, null=True)
    accomplishments = models.TextField(db_column='Accomplishments__c', blank=True, null=True)
    links = models.TextField(db_column='Links__c', blank=True, null=True)
    current_employer = models.CharField(db_column='Current_Employer__c', max_length=255, verbose_name='Current Employer', blank=True, null=True)
    preferred_work_location = models.CharField(db_column='Preferred_Work_Location__c', max_length=255, verbose_name='Preferred Work Location', blank=True, null=True)
    #current_company = models.CharField(db_column='Current_Company__c', max_length=255, verbose_name='Current Company', blank=True, null=True)
    current_role = models.CharField(db_column='Current_Role__c', max_length=255, verbose_name='Current Role', blank=True, null=True)
    expected_role = models.CharField(db_column='Expected_Role__c', max_length=255, verbose_name='Expected Role', blank=True, null=True)
    current_address = models.TextField(db_column='Current_Address__c', verbose_name='Current Address', blank=True, null=True)
    permanent_address = models.TextField(db_column='Permanent_Address__c', verbose_name='Permanent Address', blank=True, null=True)
    relevant_experience = models.CharField(db_column='Relevant_Experience__c', max_length=255, verbose_name='Relevant Experience', blank=True, null=True)
    total_experience = models.CharField(db_column='Total_Experience__c', max_length=255, verbose_name='Total Experience', blank=True, null=True)
    notice_period = models.CharField(db_column='Notice_Period__c', max_length=255, verbose_name='Notice Period', blank=True, null=True)
    screening_stages = models.CharField(db_column='Screening_Stages__c', max_length=255, verbose_name='Screening Stages', default=models.DefaultedOnCreate('Profile Created'), choices=[('Profile Created', 'Profile Created'), ('Request for Auction', 'Request for Auction'), ('BGV & Assessment', 'BGV & Assessment'), ('Ready for Auction', 'Ready for Auction')], blank=True, null=True)
    auction_availability = models.BooleanField(db_column='Auction_Availability__c', verbose_name='Auction Availability', default=models.DefaultedOnCreate(False))
    #bgv = models.BooleanField(db_column='BGV__c', verbose_name='BGV', default=models.DefaultedOnCreate(False))
    background_verification = models.BooleanField(db_column='Background_Verification__c', verbose_name='Background Verification', default=models.DefaultedOnCreate(False))

    assessment = models.CharField(db_column='Assessment__c', max_length=255, default=models.DefaultedOnCreate('Not Attempted'), choices=[('Not Attempted', 'Not Attempted'), ('Pass', 'Pass'), ('Failed', 'Failed')], blank=True, null=True)
    record_id = models.CharField(db_column='Id__c', max_length=1300, sf_read_only=models.READ_ONLY, blank=True, null=True)
    skills = models.CharField(db_column='Skills__c', max_length=255, blank=True, null=True)
    education = models.TextField(db_column='Education__c', blank=True, null=True)
    candidate_phone = models.CharField(db_column='Candidate_Phone__c', max_length=1300, verbose_name='Candidate Phone', sf_read_only=models.READ_ONLY, blank=True, null=True)
    dob = models.CharField(db_column='DOB__c', max_length=255, verbose_name='DOB', blank=True, null=True)
    class Meta(models.Model.Meta):
        db_table = 'Candidate_Profile__c'
        verbose_name = 'Candidate Profile'
        verbose_name_plural = 'Candidate Profiles'
        # keyPrefix = 'a03'



# class CandidateProfile(models.Model):
#     # owner = models.ForeignKey('Group', models.DO_NOTHING, db_column='OwnerId', verbose_name='Owner ID', default=models.DEFAULTED_ON_CREATE)  # Reference to tables [Group, User]
#     # is_deleted = models.BooleanField(db_column='IsDeleted', verbose_name='Deleted', sf_read_only=models.READ_ONLY, default=False)
#     #name = models.CharField(db_column='Name', max_length=80, verbose_name='Candidate Profile', sf_read_only=models.READ_ONLY)
#     # created_date = models.DateTimeField(db_column='CreatedDate', sf_read_only=models.READ_ONLY)
#     # created_by = models.ForeignKey('User', models.DO_NOTHING, db_column='CreatedById', related_name='candidateprofile_createdby_set', verbose_name='Created By ID', sf_read_only=models.READ_ONLY)
#     # last_modified_date = models.DateTimeField(db_column='LastModifiedDate', sf_read_only=models.READ_ONLY)
#     # last_modified_by = models.ForeignKey('User', models.DO_NOTHING, db_column='LastModifiedById', related_name='candidateprofile_lastmodifiedby_set', verbose_name='Last Modified By ID', sf_read_only=models.READ_ONLY)
#     # system_modstamp = models.DateTimeField(db_column='SystemModstamp', sf_read_only=models.READ_ONLY)
#     # last_viewed_date = models.DateTimeField(db_column='LastViewedDate', sf_read_only=models.READ_ONLY, blank=True, null=True)
#     # last_referenced_date = models.DateTimeField(db_column='LastReferencedDate', sf_read_only=models.READ_ONLY, blank=True, null=True)
#     current_employer = models.CharField(db_column='Current_Employer__c', max_length=200, verbose_name='Current Employer', blank=True, null=True)
#     current_ctc = models.DecimalField(db_column='Current_CTC__c', max_digits=18, decimal_places=2, verbose_name='Current CTC', blank=True, null=True)
#     candidate_email = models.CharField(db_column='Candidate_Email__c', max_length=1300, verbose_name='Candidate Email', sf_read_only=models.READ_ONLY, blank=True, null=True)
#     candidate = models.ForeignKey('Candidate', models.DO_NOTHING, db_column='Candidate__c', blank=True, null=True)
#     first_name = models.CharField(db_column='First_Name__c', max_length=1300, verbose_name='First Name', sf_read_only=models.READ_ONLY, blank=True, null=True)
#     last_name = models.CharField(db_column='Last_Name__c', max_length=1300, verbose_name='Last Name', sf_read_only=models.READ_ONLY, blank=True, null=True)
#     n = models.DecimalField(db_column='n__c', max_digits=18, decimal_places=0, verbose_name='No.of Auctions', default=models.DEFAULTED_ON_CREATE, blank=True, null=True)
#     resume_url = models.URLField(db_column='Resume_URL__c', verbose_name='Resume URL', blank=True, null=True)
#     about = models.TextField(db_column='About__c', blank=True, null=True)
#     skills = models.TextField(db_column='Skills__c', blank=True, null=True)
#     experience = models.TextField(db_column='Experience__c', blank=True, null=True)
#     projects = models.TextField(db_column='Projects__c', blank=True, null=True)
#     certifications = models.TextField(db_column='Certifications__c', blank=True, null=True)
#     accomplishments = models.TextField(db_column='Accomplishments__c', blank=True, null=True)
#     links = models.TextField(db_column='Links__c', blank=True, null=True)
#     preferred_work_location = models.CharField(db_column='Preferred_WorkLocation__c', max_length=255, verbose_name='Preferred WorkLocation', blank=True, null=True)
#     dob = models.DateField(db_column='DOB__c', verbose_name='DOB', blank=True, null=True)
#     current_company = models.CharField(db_column='Current_Company__c', max_length=255, verbose_name='Current Company', blank=True, null=True)
#     current_role = models.CharField(db_column='Current_Role__c', max_length=255, verbose_name='Current Role', blank=True, null=True)
#     expected_role = models.CharField(db_column='Expected_Role__c', max_length=255, verbose_name='Expected Role', blank=True, null=True)
#     current_address = models.TextField(db_column='Current_Address__c', verbose_name='Current Address', blank=True, null=True)
#     permanent_address = models.TextField(db_column='Permanent_Address__c', verbose_name='Permanent Address', blank=True, null=True)
#     relevant_experience = models.DecimalField(db_column='Relevant_Experience__c', max_digits=6, decimal_places=0, verbose_name='Relevant Experience', blank=True, null=True)
#     total_experience = models.DecimalField(db_column='Total_Experience__c', max_digits=6, decimal_places=0, verbose_name='Total Experience', blank=True, null=True)
#     notice_period = models.DecimalField(db_column='Notice_Period__c', max_digits=3, decimal_places=0, verbose_name='Notice Period', blank=True, null=True)
#     screening_stages = models.CharField(db_column='Screening_Stages__c', max_length=255, verbose_name='Screening Stages', choices=[('Profile Created', 'Profile Created'), ('Request for Auction', 'Request for Auction'), ('BGV & Assessment', 'BGV & Assessment'), ('Ready for Auction', 'Ready for Auction')], blank=True, null=True)
#     auction_availability = models.BooleanField(db_column='Auction_Availability__c', verbose_name='Auction Availability', default=models.DefaultedOnCreate(False))
#     bgv = models.BooleanField(db_column='BGV__c', verbose_name='BGV', default=models.DefaultedOnCreate(False))
#     assessment = models.CharField(db_column='Assessment__c', max_length=255, default=models.DefaultedOnCreate('Not Attempted'), choices=[('Not Attempted', 'Not Attempted'), ('Pass', 'Pass'), ('Failed', 'Failed')], blank=True, null=True)
#     record_id = models.CharField(db_column='Id__c', max_length=1300, sf_read_only=models.READ_ONLY, blank=True)
#     class Meta(models.Model.Meta):
#         db_table = 'Candidate_Profile__c'
#         verbose_name = 'Candidate Profile'
#         verbose_name_plural = 'Candidate Profiles'
#         # keyPrefix = 'a03'

class Employer(models.Model):
    #id = models.CharField(db_column='Id__c', max_length=1300, sf_read_only=models.READ_ONLY, blank=True, null=False,primary_key=True)
    #owner = models.ForeignKey('Group', models.DO_NOTHING, db_column='OwnerId', verbose_name='Owner ID', default=models.DEFAULTED_ON_CREATE)  # Reference to tables [Group, User]
    #is_deleted = models.BooleanField(db_column='IsDeleted', verbose_name='Deleted', sf_read_only=models.READ_ONLY, default=False)
    name = models.CharField(db_column='Name', max_length=80, verbose_name='Employer Name', default=models.DEFAULTED_ON_CREATE, blank=True, null=True)
    created_date = models.DateTimeField(db_column='CreatedDate', sf_read_only=models.READ_ONLY)
    #created_by = models.ForeignKey('User', models.DO_NOTHING, db_column='CreatedById', related_name='employer_createdby_set', verbose_name='Created By ID', sf_read_only=models.READ_ONLY)
    last_modified_date = models.DateTimeField(db_column='LastModifiedDate', sf_read_only=models.READ_ONLY)
    #last_modified_by = models.ForeignKey('User', models.DO_NOTHING, db_column='LastModifiedById', related_name='employer_lastmodifiedby_set', verbose_name='Last Modified By ID', sf_read_only=models.READ_ONLY)
    #system_modstamp = models.DateTimeField(db_column='SystemModstamp', sf_read_only=models.READ_ONLY)
    #last_activity_date = models.DateField(db_column='LastActivityDate', sf_read_only=models.READ_ONLY, blank=True, null=True)
    #last_viewed_date = models.DateTimeField(db_column='LastViewedDate', sf_read_only=models.READ_ONLY, blank=True, null=True)
    #last_referenced_date = models.DateTimeField(db_column='LastReferencedDate', sf_read_only=models.READ_ONLY, blank=True, null=True)
    communication_email = models.EmailField(db_column='Communication_Email__c', unique=True, verbose_name='Communication Email')
    screening_stage = models.CharField(db_column='Screening_Stage__c', max_length=255, verbose_name='Screening Stage', choices=[('Draft', 'Draft'), ('Background Check', 'Background Check'), ('Proposal', 'Proposal'), ('Negotiation', 'Negotiation'), ('Accept', 'Accept'), ('Reject', 'Reject')], blank=True, null=True)
    phone = models.CharField(db_column='Phone__c', max_length=40)
    website = models.URLField(db_column='Website__c')
    email_verification = models.BooleanField(db_column='Email_Verification__c', verbose_name='Email Verification', default=models.DefaultedOnCreate(False))
    record_id = models.CharField(db_column='Record_ID__c', max_length=1300, verbose_name='Record ID', sf_read_only=models.READ_ONLY, blank=True, null=True)
    password = models.CharField(db_column='Password__c', max_length=255, blank=True, null=True)
    ceo_validated = models.CharField(db_column='CEO_Validated__c', max_length=255, verbose_name='CEO Validated', choices=[('Yes', 'Yes'), ('No', 'No')], blank=True, null=True)
    class Meta(models.Model.Meta):
        db_table = 'Employer__c'
        verbose_name = 'Employer'
        verbose_name_plural = 'Employers'
        # keyPrefix = 'a00'

class EmployerProfile(models.Model):
    #owner = models.ForeignKey('Group', models.DO_NOTHING, db_column='OwnerId', verbose_name='Owner ID', default=models.DEFAULTED_ON_CREATE)  # Reference to tables [Group, User]
    #is_deleted = models.BooleanField(db_column='IsDeleted', verbose_name='Deleted', sf_read_only=models.READ_ONLY, default=False)
    #name = models.CharField(db_column='Name', max_length=80, verbose_name='Employer Profile Name', sf_read_only=models.READ_ONLY)
    created_date = models.DateTimeField(db_column='CreatedDate', sf_read_only=models.READ_ONLY)
    #created_by = models.ForeignKey('User', models.DO_NOTHING, db_column='CreatedById', related_name='employerprofile_createdby_set', verbose_name='Created By ID', sf_read_only=models.READ_ONLY)
    #last_modified_date = models.DateTimeField(db_column='LastModifiedDate', sf_read_only=models.READ_ONLY)
    #last_modified_by = models.ForeignKey('User', models.DO_NOTHING, db_column='LastModifiedById', related_name='employerprofile_lastmodifiedby_set', verbose_name='Last Modified By ID', sf_read_only=models.READ_ONLY)
    #system_modstamp = models.DateTimeField(db_column='SystemModstamp', sf_read_only=models.READ_ONLY)
    #last_activity_date = models.DateField(db_column='LastActivityDate', sf_read_only=models.READ_ONLY, blank=True, null=True)
    #last_viewed_date = models.DateTimeField(db_column='LastViewedDate', sf_read_only=models.READ_ONLY, blank=True, null=True)
    #last_referenced_date = models.DateTimeField(db_column='LastReferencedDate', sf_read_only=models.READ_ONLY, blank=True, null=True)
    employer = models.ForeignKey('Employer', models.DO_NOTHING, db_column='Employer__c', blank=True, null=True)
    communication_email = models.CharField(db_column='Communication_Email__c', max_length=1300, verbose_name='Communication Email', sf_read_only=models.READ_ONLY, blank=True, null=True)
    phone = models.CharField(db_column='Phone__c', max_length=1300, sf_read_only=models.READ_ONLY, blank=True, null=True)
    class Meta(models.Model.Meta):
        db_table = 'Employer_Profile__c'
        verbose_name = 'Employer Profile'
        verbose_name_plural = 'Employer Profiles'
        # keyPrefix = 'a07'



# class ResetPassword(models.Model):
#     # owner = models.ForeignKey(Group, models.DO_NOTHING, db_column='OwnerId', verbose_name='Owner ID', default=models.DEFAULTED_ON_CREATE)  # Reference to tables [Group, User]
#     is_deleted = models.BooleanField(db_column='IsDeleted', verbose_name='Deleted', sf_read_only=models.READ_ONLY, default=False)
#     name = models.CharField(db_column='Name', max_length=80, verbose_name='Password Reset Name', sf_read_only=models.READ_ONLY)
#     created_date = models.DateTimeField(db_column='CreatedDate', sf_read_only=models.READ_ONLY)
#     # created_by = models.ForeignKey('User', models.DO_NOTHING, db_column='CreatedById', related_name='resetpassword_createdby_set', verbose_name='Created By ID', sf_read_only=models.READ_ONLY)
#     last_modified_date = models.DateTimeField(db_column='LastModifiedDate', sf_read_only=models.READ_ONLY)
#     # last_modified_by = models.ForeignKey('User', models.DO_NOTHING, db_column='LastModifiedById', related_name='resetpassword_lastmodifiedby_set', verbose_name='Last Modified By ID', sf_read_only=models.READ_ONLY)
#     system_modstamp = models.DateTimeField(db_column='SystemModstamp', sf_read_only=models.READ_ONLY)
#     reset_token = models.CharField(db_column='Reset_Token__c', max_length=255, verbose_name='Reset Token', blank=True, null=True)
#     candidate = models.ForeignKey(Candidate, models.DO_NOTHING, db_column='Candidate__c', blank=True, null=True)
#     employer = models.ForeignKey(Employer, models.DO_NOTHING, db_column='Employer__c', blank=True, null=True)
#     class Meta(models.Model.Meta):
#         db_table = 'Reset_Password__c'
#         verbose_name = 'Reset Password'
#         verbose_name_plural = 'Reset Passwords'
#         # keyPrefix = 'a05'

# class Verification(models.Model):
#     # owner = models.ForeignKey(Group, models.DO_NOTHING, db_column='OwnerId', verbose_name='Owner ID', default=models.DEFAULTED_ON_CREATE)  # Reference to tables [Group, User]
#     is_deleted = models.BooleanField(db_column='IsDeleted', verbose_name='Deleted', sf_read_only=models.READ_ONLY, default=False)
#     name = models.CharField(db_column='Name', max_length=80, verbose_name='Verification Name', sf_read_only=models.READ_ONLY)
#     created_date = models.DateTimeField(db_column='CreatedDate', sf_read_only=models.READ_ONLY)
#     # created_by = models.ForeignKey(User, models.DO_NOTHING, db_column='CreatedById', related_name='verification_createdby_set', verbose_name='Created By ID', sf_read_only=models.READ_ONLY)
#     last_modified_date = models.DateTimeField(db_column='LastModifiedDate', sf_read_only=models.READ_ONLY)
#     # last_modified_by = models.ForeignKey(User, models.DO_NOTHING, db_column='LastModifiedById', related_name='verification_lastmodifiedby_set', verbose_name='Last Modified By ID', sf_read_only=models.READ_ONLY)
#     system_modstamp = models.DateTimeField(db_column='SystemModstamp', sf_read_only=models.READ_ONLY)
#     last_activity_date = models.DateField(db_column='LastActivityDate', sf_read_only=models.READ_ONLY, blank=True, null=True)
#     last_viewed_date = models.DateTimeField(db_column='LastViewedDate', sf_read_only=models.READ_ONLY, blank=True, null=True)
#     last_referenced_date = models.DateTimeField(db_column='LastReferencedDate', sf_read_only=models.READ_ONLY, blank=True, null=True)
#     verify_token = models.CharField(db_column='Verify_Token__c', max_length=255, verbose_name='Verify Token', blank=True, null=True)
#     candidate = models.ForeignKey(Candidate, models.DO_NOTHING, db_column='Candidate__c', blank=True, null=True)
#     employer = models.ForeignKey(Employer, models.DO_NOTHING, db_column='Employer__c', blank=True, null=True)
#     class Meta(models.Model.Meta):
#         db_table = 'Verification__c'
#         verbose_name = 'Verification'
#         verbose_name_plural = 'Verifications'
#         # keyPrefix = 'a06'


class Account(models.Model):
    # is_deleted = models.BooleanField(db_column='IsDeleted', verbose_name='Deleted', sf_read_only=models.READ_ONLY, default=False)
    # master_record = models.ForeignKey('self', models.DO_NOTHING, db_column='MasterRecordId', related_name='account_masterrecord_set', verbose_name='Master Record ID', sf_read_only=models.READ_ONLY, blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=255, verbose_name='Employer Name')
    type = models.CharField(db_column='Type', max_length=255, verbose_name='Employer Type', choices=[('Service Based', 'Service Based'), ('Product Based', 'Product Based'), ('IT', 'IT'), ('Banking', 'Banking')], blank=True, null=True)
    # parent = models.ForeignKey('self', models.DO_NOTHING, db_column='ParentId', related_name='account_parent_set', verbose_name='Parent Account ID', blank=True, null=True)
    # billing_street = models.TextField(db_column='BillingStreet', blank=True, null=True)
    # billing_city = models.CharField(db_column='BillingCity', max_length=40, blank=True, null=True)
    # billing_state = models.CharField(db_column='BillingState', max_length=80, verbose_name='Billing State/Province', blank=True, null=True)
    # billing_postal_code = models.CharField(db_column='BillingPostalCode', max_length=20, verbose_name='Billing Zip/Postal Code', blank=True, null=True)
    # billing_country = models.CharField(db_column='BillingCountry', max_length=80, blank=True, null=True)
    # billing_latitude = models.DecimalField(db_column='BillingLatitude', max_digits=18, decimal_places=15, blank=True, null=True)
    # billing_longitude = models.DecimalField(db_column='BillingLongitude', max_digits=18, decimal_places=15, blank=True, null=True)
    # billing_geocode_accuracy = models.CharField(db_column='BillingGeocodeAccuracy', max_length=40, choices=[('Address', 'Address'), ('NearAddress', 'NearAddress'), ('Block', 'Block'), ('Street', 'Street'), ('ExtendedZip', 'ExtendedZip'), ('Zip', 'Zip'), ('Neighborhood', 'Neighborhood'), ('City', 'City'), ('County', 'County'), ('State', 'State'), ('Unknown', 'Unknown')], blank=True, null=True)
    billing_address = models.TextField(db_column='BillingAddress', verbose_name='Office Address', sf_read_only=models.READ_ONLY, blank=True, null=True)  # This field type is a guess.
    # shipping_street = models.TextField(db_column='ShippingStreet', blank=True, null=True)
    # shipping_city = models.CharField(db_column='ShippingCity', max_length=40, blank=True, null=True)
    # shipping_state = models.CharField(db_column='ShippingState', max_length=80, verbose_name='Shipping State/Province', blank=True, null=True)
    # shipping_postal_code = models.CharField(db_column='ShippingPostalCode', max_length=20, verbose_name='Shipping Zip/Postal Code', blank=True, null=True)
    # shipping_country = models.CharField(db_column='ShippingCountry', max_length=80, blank=True, null=True)
    # shipping_latitude = models.DecimalField(db_column='ShippingLatitude', max_digits=18, decimal_places=15, blank=True, null=True)
    # shipping_longitude = models.DecimalField(db_column='ShippingLongitude', max_digits=18, decimal_places=15, blank=True, null=True)
    # shipping_geocode_accuracy = models.CharField(db_column='ShippingGeocodeAccuracy', max_length=40, choices=[('Address', 'Address'), ('NearAddress', 'NearAddress'), ('Block', 'Block'), ('Street', 'Street'), ('ExtendedZip', 'ExtendedZip'), ('Zip', 'Zip'), ('Neighborhood', 'Neighborhood'), ('City', 'City'), ('County', 'County'), ('State', 'State'), ('Unknown', 'Unknown')], blank=True, null=True)
    # shipping_address = models.TextField(db_column='ShippingAddress', sf_read_only=models.READ_ONLY, blank=True, null=True)  # This field type is a guess.
    #phone = models.CharField(db_column='Phone', max_length=40, verbose_name='Account Phone', blank=True, null=True)
    # fax = models.CharField(db_column='Fax', max_length=40, verbose_name='Account Fax', blank=True, null=True)
    # account_number = models.CharField(db_column='AccountNumber', max_length=40, blank=True, null=True)
    website = models.URLField(db_column='Website', blank=True, null=True)
    # photo_url = models.URLField(db_column='PhotoUrl', verbose_name='Photo URL', sf_read_only=models.READ_ONLY, blank=True, null=True)
    # sic = models.CharField(db_column='Sic', max_length=20, verbose_name='SIC Code', blank=True, null=True)
    # industry = models.CharField(db_column='Industry', max_length=255, choices=[('Agriculture', 'Agriculture'), ('Apparel', 'Apparel'), ('Banking', 'Banking'), ('Biotechnology', 'Biotechnology'), ('Chemicals', 'Chemicals'), ('Communications', 'Communications'), ('Construction', 'Construction'), ('Consulting', 'Consulting'), ('Education', 'Education'), ('Electronics', 'Electronics'), ('Energy', 'Energy'), ('Engineering', 'Engineering'), ('Entertainment', 'Entertainment'), ('Environmental', 'Environmental'), ('Finance', 'Finance'), ('Food & Beverage', 'Food & Beverage'), ('Government', 'Government'), ('Healthcare', 'Healthcare'), ('Hospitality', 'Hospitality'), ('Insurance', 'Insurance'), ('Machinery', 'Machinery'), ('Manufacturing', 'Manufacturing'), ('Media', 'Media'), ('Not For Profit', 'Not For Profit'), ('Recreation', 'Recreation'), ('Retail', 'Retail'), ('Shipping', 'Shipping'), ('Technology', 'Technology'), ('Telecommunications', 'Telecommunications'), ('Transportation', 'Transportation'), ('Utilities', 'Utilities'), ('Other', 'Other')], blank=True, null=True)
    # annual_revenue = models.DecimalField(db_column='AnnualRevenue', max_digits=18, decimal_places=0, blank=True, null=True)
    number_of_employees = models.IntegerField(db_column='NumberOfEmployees', verbose_name='Total Employees', blank=True, null=True)
    # ownership = models.CharField(db_column='Ownership', max_length=255, choices=[('Public', 'Public'), ('Private', 'Private'), ('Subsidiary', 'Subsidiary'), ('Other', 'Other')], blank=True, null=True)
    # ticker_symbol = models.CharField(db_column='TickerSymbol', max_length=20, blank=True, null=True)
    # description = models.TextField(db_column='Description', verbose_name='Account Description', blank=True, null=True)
    # rating = models.CharField(db_column='Rating', max_length=255, verbose_name='Account Rating', choices=[('Hot', 'Hot'), ('Warm', 'Warm'), ('Cold', 'Cold')], blank=True, null=True)
    # site = models.CharField(db_column='Site', max_length=80, verbose_name='Account Site', blank=True, null=True)
    # owner = models.ForeignKey('User', models.DO_NOTHING, db_column='OwnerId', related_name='account_owner_set', verbose_name='Owner ID', default=models.DEFAULTED_ON_CREATE)
    # created_date = models.DateTimeField(db_column='CreatedDate', sf_read_only=models.READ_ONLY)
    # created_by = models.ForeignKey('User', models.DO_NOTHING, db_column='CreatedById', related_name='account_createdby_set', verbose_name='Created By ID', sf_read_only=models.READ_ONLY)
    # last_modified_date = models.DateTimeField(db_column='LastModifiedDate', sf_read_only=models.READ_ONLY)
    # last_modified_by = models.ForeignKey('User', models.DO_NOTHING, db_column='LastModifiedById', related_name='account_lastmodifiedby_set', verbose_name='Last Modified By ID', sf_read_only=models.READ_ONLY)
    # system_modstamp = models.DateTimeField(db_column='SystemModstamp', sf_read_only=models.READ_ONLY)
    # last_activity_date = models.DateField(db_column='LastActivityDate', verbose_name='Last Activity', sf_read_only=models.READ_ONLY, blank=True, null=True)
    # last_viewed_date = models.DateTimeField(db_column='LastViewedDate', sf_read_only=models.READ_ONLY, blank=True, null=True)
    # last_referenced_date = models.DateTimeField(db_column='LastReferencedDate', sf_read_only=models.READ_ONLY, blank=True, null=True)
    # jigsaw = models.CharField(db_column='Jigsaw', max_length=20, verbose_name='Data.com Key', blank=True, null=True)
    # jigsaw_company_id = models.CharField(db_column='JigsawCompanyId', max_length=20, verbose_name='Jigsaw Company ID', sf_read_only=models.READ_ONLY, blank=True, null=True)
    # clean_status = models.CharField(db_column='CleanStatus', max_length=40, choices=[('Matched', 'In Sync'), ('Different', 'Different'), ('Acknowledged', 'Reviewed'), ('NotFound', 'Not Found'), ('Inactive', 'Inactive'), ('Pending', 'Not Compared'), ('SelectMatch', 'Select Match'), ('Skipped', 'Skipped')], blank=True, null=True)
    # account_source = models.CharField(db_column='AccountSource', max_length=255, choices=[('Web', 'Web'), ('Phone Inquiry', 'Phone Inquiry'), ('Partner Referral', 'Partner Referral'), ('Purchased List', 'Purchased List'), ('Other', 'Other')], blank=True, null=True)
    # duns_number = models.CharField(db_column='DunsNumber', max_length=9, verbose_name='D-U-N-S Number', blank=True, null=True)
    # tradestyle = models.CharField(db_column='Tradestyle', max_length=255, blank=True, null=True)
    # naics_code = models.CharField(db_column='NaicsCode', max_length=8, verbose_name='NAICS Code', blank=True, null=True)
    # naics_desc = models.CharField(db_column='NaicsDesc', max_length=120, verbose_name='NAICS Description', blank=True, null=True)
    # year_started = models.CharField(db_column='YearStarted', max_length=4, blank=True, null=True)
    # sic_desc = models.CharField(db_column='SicDesc', max_length=80, verbose_name='SIC Description', blank=True, null=True)
    # dandb_company = models.ForeignKey('DandBcompany', models.DO_NOTHING, db_column='DandbCompanyId', verbose_name='D&B Company ID', blank=True, null=True)
    # customer_priority = models.CharField(db_column='CustomerPriority__c', max_length=255, choices=[('High', 'High'), ('Low', 'Low'), ('Medium', 'Medium')], blank=True, null=True)
    # sla = models.CharField(db_column='SLA__c', max_length=255, verbose_name='SLA', choices=[('Gold', 'Gold'), ('Silver', 'Silver'), ('Platinum', 'Platinum'), ('Bronze', 'Bronze')], blank=True, null=True)
    #active = models.CharField(db_column='Active__c', max_length=255, choices=[('No', 'No'), ('Yes', 'Yes')], blank=True, null=True)
    # numberof_locations = models.DecimalField(db_column='NumberofLocations__c', max_digits=3, decimal_places=0, verbose_name='Number of Locations', blank=True, null=True)
    # upsell_opportunity = models.CharField(db_column='UpsellOpportunity__c', max_length=255, choices=[('Maybe', 'Maybe'), ('No', 'No'), ('Yes', 'Yes')], blank=True, null=True)
    # slaserial_number = models.CharField(db_column='SLASerialNumber__c', max_length=10, verbose_name='SLA Serial Number', blank=True, null=True)
    # slaexpiration_date = models.DateField(db_column='SLAExpirationDate__c', verbose_name='SLA Expiration Date', blank=True, null=True)
    #skills = models.CharField(db_column='Skills__c', max_length=4099, choices=[('C', 'C'), ('C++', 'C++'), ('Java', 'Java'), ('Python', 'Python')], blank=True, null=True)
    created_date = models.DateTimeField(db_column='CreatedDate', sf_read_only=models.READ_ONLY, null=True)
    bgv_completed = models.BooleanField(db_column='BGV_Completed__c', verbose_name='BGV Completed', default=models.DefaultedOnCreate(False))
    employer_team_count = models.DecimalField(db_column='Employer_Team_Count__c', max_digits=18, decimal_places=0, verbose_name='Employer Team Count', default=models.DEFAULTED_ON_CREATE, blank=True, null=True)
    employer_details_id = models.CharField(db_column='Employer_Details_Id__c', max_length=1300, verbose_name='Employer Details Id', sf_read_only=models.READ_ONLY, blank=True, null=True)
    class Meta(models.Model.Meta):
        db_table = 'Account'
        verbose_name = 'Employer Detail'
        verbose_name_plural = 'Employer Details'
        # keyPrefix = '001'



class Contact(models.Model):
    #is_deleted = models.BooleanField(db_column='IsDeleted', verbose_name='Deleted', sf_read_only=models.READ_ONLY, default=False)
    #master_record = models.ForeignKey('self', models.DO_NOTHING, db_column='MasterRecordId', related_name='contact_masterrecord_set', verbose_name='Master Record ID', sf_read_only=models.READ_ONLY, blank=True, null=True)
    account = models.ForeignKey(Account, models.DO_NOTHING, db_column='AccountId', verbose_name='Employer Name', blank=True, null=True)  # Master Detail Relationship *
    last_name = models.CharField(db_column='LastName', max_length=80)
    first_name = models.CharField(db_column='FirstName', max_length=40, blank=True, null=True)
    created_date = models.DateTimeField(db_column='CreatedDate', sf_read_only=models.READ_ONLY, null= True)
    #salutation = models.CharField(db_column='Salutation', max_length=40, choices=[('Mr.', 'Mr.'), ('Ms.', 'Ms.'), ('Mrs.', 'Mrs.'), ('Dr.', 'Dr.'), ('Prof.', 'Prof.')], blank=True, null=True)
    #name = models.CharField(db_column='Name', max_length=121, verbose_name='Full Name', sf_read_only=models.READ_ONLY)
    #other_street = models.TextField(db_column='OtherStreet', blank=True, null=True)
    #other_city = models.CharField(db_column='OtherCity', max_length=40, blank=True, null=True)
    #other_state = models.CharField(db_column='OtherState', max_length=80, verbose_name='Other State/Province', blank=True, null=True)
    #other_postal_code = models.CharField(db_column='OtherPostalCode', max_length=20, verbose_name='Other Zip/Postal Code', blank=True, null=True)
    #other_country = models.CharField(db_column='OtherCountry', max_length=80, blank=True, null=True)
    #other_latitude = models.DecimalField(db_column='OtherLatitude', max_digits=18, decimal_places=15, blank=True, null=True)
    #other_longitude = models.DecimalField(db_column='OtherLongitude', max_digits=18, decimal_places=15, blank=True, null=True)
    #other_geocode_accuracy = models.CharField(db_column='OtherGeocodeAccuracy', max_length=40, choices=[('Address', 'Address'), ('NearAddress', 'NearAddress'), ('Block', 'Block'), ('Street', 'Street'), ('ExtendedZip', 'ExtendedZip'), ('Zip', 'Zip'), ('Neighborhood', 'Neighborhood'), ('City', 'City'), ('County', 'County'), ('State', 'State'), ('Unknown', 'Unknown')], blank=True, null=True)
    #other_address = models.TextField(db_column='OtherAddress', sf_read_only=models.READ_ONLY, blank=True, null=True)  # This field type is a guess.
    #mailing_street = models.TextField(db_column='MailingStreet', blank=True, null=True)
    #mailing_city = models.CharField(db_column='MailingCity', max_length=40, blank=True, null=True)
    #mailing_state = models.CharField(db_column='MailingState', max_length=80, verbose_name='Mailing State/Province', blank=True, null=True)
    #mailing_postal_code = models.CharField(db_column='MailingPostalCode', max_length=20, verbose_name='Mailing Zip/Postal Code', blank=True, null=True)
    #mailing_country = models.CharField(db_column='MailingCountry', max_length=80, blank=True, null=True)
    #mailing_latitude = models.DecimalField(db_column='MailingLatitude', max_digits=18, decimal_places=15, blank=True, null=True)
    #mailing_longitude = models.DecimalField(db_column='MailingLongitude', max_digits=18, decimal_places=15, blank=True, null=True)
    #mailing_geocode_accuracy = models.CharField(db_column='MailingGeocodeAccuracy', max_length=40, choices=[('Address', 'Address'), ('NearAddress', 'NearAddress'), ('Block', 'Block'), ('Street', 'Street'), ('ExtendedZip', 'ExtendedZip'), ('Zip', 'Zip'), ('Neighborhood', 'Neighborhood'), ('City', 'City'), ('County', 'County'), ('State', 'State'), ('Unknown', 'Unknown')], blank=True, null=True)
    #mailing_address = models.TextField(db_column='MailingAddress', sf_read_only=models.READ_ONLY, blank=True, null=True)  # This field type is a guess.
    #phone = models.CharField(db_column='Phone', max_length=40, verbose_name='Business Phone', blank=True, null=True)
    #fax = models.CharField(db_column='Fax', max_length=40, verbose_name='Business Fax', blank=True, null=True)
    mobile_phone = models.CharField(db_column='MobilePhone', max_length=40, blank=True, null=True)
    #home_phone = models.CharField(db_column='HomePhone', max_length=40, blank=True, null=True)
    #other_phone = models.CharField(db_column='OtherPhone', max_length=40, blank=True, null=True)
    #assistant_phone = models.CharField(db_column='AssistantPhone', max_length=40, verbose_name='Asst. Phone', blank=True, null=True)
    #reports_to = models.ForeignKey('self', models.DO_NOTHING, db_column='ReportsToId', related_name='contact_reportsto_set', verbose_name='Reports To ID', blank=True, null=True)
    email = models.EmailField(db_column='Email', blank=True, null=True)
    #title = models.CharField(db_column='Title', max_length=128, blank=True, null=True)
    #department = models.CharField(db_column='Department', max_length=80, blank=True, null=True)
    #assistant_name = models.CharField(db_column='AssistantName', max_length=40, verbose_name="Assistant's Name", blank=True, null=True)
    #lead_source = models.CharField(db_column='LeadSource', max_length=255, choices=[('Web', 'Web'), ('Phone Inquiry', 'Phone Inquiry'), ('Partner Referral', 'Partner Referral'), ('Purchased List', 'Purchased List'), ('Other', 'Other')], blank=True, null=True)
    #birthdate = models.DateField(db_column='Birthdate', blank=True, null=True)
    #description = models.TextField(db_column='Description', verbose_name='Contact Description', blank=True, null=True)
    #owner = models.ForeignKey('User', models.DO_NOTHING, db_column='OwnerId', related_name='contact_owner_set', verbose_name='Owner ID', default=models.DEFAULTED_ON_CREATE)
    #created_date = models.DateTimeField(db_column='CreatedDate', sf_read_only=models.READ_ONLY)
    #created_by = models.ForeignKey('User', models.DO_NOTHING, db_column='CreatedById', related_name='contact_createdby_set', verbose_name='Created By ID', sf_read_only=models.READ_ONLY)
    #last_modified_date = models.DateTimeField(db_column='LastModifiedDate', sf_read_only=models.READ_ONLY)
    #last_modified_by = models.ForeignKey('User', models.DO_NOTHING, db_column='LastModifiedById', related_name='contact_lastmodifiedby_set', verbose_name='Last Modified By ID', sf_read_only=models.READ_ONLY)
    #system_modstamp = models.DateTimeField(db_column='SystemModstamp', sf_read_only=models.READ_ONLY)
    #last_activity_date = models.DateField(db_column='LastActivityDate', verbose_name='Last Activity', sf_read_only=models.READ_ONLY, blank=True, null=True)
    #last_curequest_date = models.DateTimeField(db_column='LastCURequestDate', verbose_name='Last Stay-in-Touch Request Date', sf_read_only=models.READ_ONLY, blank=True, null=True)
    #last_cuupdate_date = models.DateTimeField(db_column='LastCUUpdateDate', verbose_name='Last Stay-in-Touch Save Date', sf_read_only=models.READ_ONLY, blank=True, null=True)
    #last_viewed_date = models.DateTimeField(db_column='LastViewedDate', sf_read_only=models.READ_ONLY, blank=True, null=True)
    #last_referenced_date = models.DateTimeField(db_column='LastReferencedDate', sf_read_only=models.READ_ONLY, blank=True, null=True)
    #email_bounced_reason = models.CharField(db_column='EmailBouncedReason', max_length=255, blank=True, null=True)
    #email_bounced_date = models.DateTimeField(db_column='EmailBouncedDate', blank=True, null=True)
    #is_email_bounced = models.BooleanField(db_column='IsEmailBounced', sf_read_only=models.READ_ONLY, default=False)
    #photo_url = models.URLField(db_column='PhotoUrl', verbose_name='Photo URL', sf_read_only=models.READ_ONLY, blank=True, null=True)
    #jigsaw = models.CharField(db_column='Jigsaw', max_length=20, verbose_name='Data.com Key', blank=True, null=True)
    #jigsaw_contact_id = models.CharField(db_column='JigsawContactId', max_length=20, verbose_name='Jigsaw Contact ID', sf_read_only=models.READ_ONLY, blank=True, null=True)
    #clean_status = models.CharField(db_column='CleanStatus', max_length=40, choices=[('Matched', 'In Sync'), ('Different', 'Different'), ('Acknowledged', 'Reviewed'), ('NotFound', 'Not Found'), ('Inactive', 'Inactive'), ('Pending', 'Not Compared'), ('SelectMatch', 'Select Match'), ('Skipped', 'Skipped')], blank=True, null=True)
    #individual = models.ForeignKey('Individual', models.DO_NOTHING, db_column='IndividualId', verbose_name='Individual ID', blank=True, null=True)
    #level = models.CharField(db_column='Level__c', max_length=255, choices=[('Secondary', 'Secondary'), ('Tertiary', 'Tertiary'), ('Primary', 'Primary')], blank=True, null=True)
    #languages = models.CharField(db_column='Languages__c', max_length=100, blank=True, null=True)
    email_verified = models.BooleanField(db_column='Email_Verified__c', verbose_name='Email Verified', default=models.DefaultedOnCreate(False))
    password = models.CharField(db_column='Password__c', max_length=255)
    role = models.CharField(db_column='Role__c', max_length=255, choices=[('Admin', 'Admin'), ('Team Member', 'Team Member')], blank=True, null=True)
    member_id = models.CharField(db_column='Member_Id__c', max_length=1300, verbose_name='Member Id', sf_read_only=models.READ_ONLY, blank=True, null=True)
    status = models.CharField(db_column='Status__c', max_length=255, default=models.DefaultedOnCreate('Active'), choices=[('Active', 'Active'), ('Inactive', 'Inactive')], blank=True, null=True)

    class Meta(models.Model.Meta):
        db_table = 'Contact'
        verbose_name = 'Employer Team'
        verbose_name_plural = 'Employer Teams'
        # keyPrefix = '003'

class Notification(models.Model):
    # is_deleted = models.BooleanField(db_column='IsDeleted', verbose_name='Deleted', sf_read_only=models.READ_ONLY, default=False)
    # name = models.CharField(db_column='Name', max_length=80, verbose_name='Notification Name', sf_read_only=models.READ_ONLY)
    created_date = models.DateTimeField(db_column='CreatedDate', sf_read_only=models.READ_ONLY)
    # created_by = models.ForeignKey('User', models.DO_NOTHING, db_column='CreatedById', related_name='notification_createdby_set', verbose_name='Created By ID', sf_read_only=models.READ_ONLY)
    # last_modified_date = models.DateTimeField(db_column='LastModifiedDate', sf_read_only=models.READ_ONLY)
    # last_modified_by = models.ForeignKey('User', models.DO_NOTHING, db_column='LastModifiedById', related_name='notification_lastmodifiedby_set', verbose_name='Last Modified By ID', sf_read_only=models.READ_ONLY)
    # system_modstamp = models.DateTimeField(db_column='SystemModstamp', sf_read_only=models.READ_ONLY)
    # last_activity_date = models.DateField(db_column='LastActivityDate', sf_read_only=models.READ_ONLY, blank=True, null=True)
    # last_viewed_date = models.DateTimeField(db_column='LastViewedDate', sf_read_only=models.READ_ONLY, blank=True, null=True)
    # last_referenced_date = models.DateTimeField(db_column='LastReferencedDate', sf_read_only=models.READ_ONLY, blank=True, null=True)
    # employer_details = models.ForeignKey(Account, models.DO_NOTHING, db_column='Employer_Details__c', verbose_name='Employer Details', sf_read_only=models.NOT_UPDATEABLE)  # Master Detail Relationship 0
    employer_team = models.ForeignKey(Contact, models.DO_NOTHING, db_column='Employer_Team__c', verbose_name='Employer Team', blank=True, null=True)
    message = models.TextField(db_column='Message__c', blank=True, null=True)
    read = models.BooleanField(db_column='Read__c', default=models.DefaultedOnCreate(False))
    class Meta(models.Model.Meta):
        db_table = 'Notification__c'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_date']

        # keyPrefix = 'a07'