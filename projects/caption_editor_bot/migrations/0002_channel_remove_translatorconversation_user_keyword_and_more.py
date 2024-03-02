# Generated by Django 5.0.1 on 2024-03-02 21:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caption_editor_bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('channel_id', models.CharField(blank=True, max_length=200, null=True)),
                ('channel_sign', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='translatorconversation',
            name='user',
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('channel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='caption_editor_bot.channel')),
            ],
            options={
                'unique_together': {('text', 'channel')},
            },
        ),
        migrations.DeleteModel(
            name='TelegramProfile',
        ),
        migrations.DeleteModel(
            name='TranslatorConversation',
        ),
    ]