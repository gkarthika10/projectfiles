from django.dispatch import receiver
from .models import SchedulerInterval
from django.db.models.signals import post_save
from django_celery_beat.models import PeriodicTask, IntervalSchedule
 

  
@receiver(post_save, sender=SchedulerInterval)
def save_profile(sender, instance, created, **kwargs):

    if not created and instance.name == "dashboard_cache":

        task = "opscentre_usermanagement_api.tasks.update_dashboard_cache"
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=int(instance.interval),
            period=IntervalSchedule.MINUTES,
        )

        PeriodicTask.objects.create(
            interval=schedule,                       # we created this above.
            name='Update Dasboard Cache Table',      # simply describes this periodic task.
            task=task,                               # name of task.
        )   