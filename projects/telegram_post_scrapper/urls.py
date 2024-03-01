from django.urls import path

from .views import channels_to_json, client_settings_to_json, bot_to_json, channel_type_to_json, \
    keyword_channel_ads_to_json, all_url_list_html

urlpatterns = [
    path('channels/json/', channels_to_json, name='channels_to_json'),
    path('client_settings/json/', client_settings_to_json, name='client_settings_to_json'),
    path('bot/json/', bot_to_json, name='bot_to_json'),
    path('channel_type/json/', channel_type_to_json, name='channel_type_to_json'),
    path('keyword/json/', keyword_channel_ads_to_json, name='keyword_to_json'),
    path('config/url/list/json/', all_url_list_html, name='all_url_list_html'),
]
