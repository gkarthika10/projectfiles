from django.apps import AppConfig


class OpscentreUsermanagementApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'opscentre_usermanagement_api'

    def ready(self):
        import opscentre_usermanagement_api.signals
