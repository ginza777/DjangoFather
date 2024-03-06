from django.urls import path
from central_system.views import ChannelsApi, ClientSettingsApi, BotApi, ChannelTypeApi, KeywordChannelAdsApi

urlpatterns = [
    path('channels/', ChannelsApi.as_view(), name='channels_to_json'),
    path('client_settings/', ClientSettingsApi.as_view(), name='client_settings_to_json'),
    path('bot/', BotApi.as_view(), name='bot_to_json'),
    path('channel_type/', ChannelTypeApi.as_view(), name='channel_type_to_json'),
    path('keyword/', KeywordChannelAdsApi.as_view(), name='keyword_to_json'),
]