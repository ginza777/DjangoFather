from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .webhook import handle_telegram_webhook
from .apps import CommonBotConfig
app_name = CommonBotConfig.name.split(".")[1]
print(100*"#")
print(f"url: {app_name}/handle_telegram_webhook/")
urlpatterns = [
    path(f"{app_name}/handle_telegram_webhook/<str:bot_token>", csrf_exempt(handle_telegram_webhook), name="telegram_webhook")
]
