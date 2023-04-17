import requests
from decouple import config
from .models import DashboardCache
from kyw_api_project.celery import app 


@app.task
def update_dashboard_cache():
    base_domain = config("BASE_DOMAIN")
    url = f"{base_domain}/api/ops/auth/dashboard"
    response = requests.get(url).json()
    for key, value in response.items():
        DashboardCache.objects.filter(name=key).update(count=value)
