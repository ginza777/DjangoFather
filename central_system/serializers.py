from rest_framework import serializers
from projects.telegram_post_scrapper.models import Client_Settings,Channel_post_setting, Bot, Channel_type, Channels, KeywordChannelAds


class ChannelsSerializer(serializers.ModelSerializer):
    bot_data = serializers.SerializerMethodField()
    channel_type = serializers.SerializerMethodField()
    channel_post_setting = serializers.SerializerMethodField()
    class Meta:
        model = Channels
        fields = (
            "channel_name",
            "channel_link",
            "channel_id",
            "my_channel",
            "bot",
            "type",
            "setting",
            "created_at",
            "updated_at",
            "bot_data",
            "channel_type",
            "channel_post_setting",
        )

    def get_bot_data(self, obj):
        return BotSerializer(obj.bot).data

    def get_channel_type(self, obj):
        return ChannelTypeSerializer(obj.type).data

    def get_channel_post_setting(self, obj):
        return ChannelPostSettingSerializer(obj.setting).data

class ClientSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client_Settings
        fields = '__all__'


class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = '__all__'

class ChannelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel_type
        fields = '__all__'

class KeywordChannelAdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeywordChannelAds
        fields = '__all__'

class ChannelPostSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel_post_setting
        fields = '__all__'