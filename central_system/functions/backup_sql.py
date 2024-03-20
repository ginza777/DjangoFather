import datetime
import os
import subprocess
import shutil
import environ
import time
from central_system.models import LogSenderBot, BackupDbBot
from central_system.views import send_to_telegram, send_msg_log

env = environ.Env()
env.read_env(".env")


# Corrected class name to "Commands"


def backup_database():
    try:

        DB_NAME = env.str("DB_NAME")
        DB_USER = env.str("DB_USER")
        DB_PASSWORD = env.str("DB_PASSWORD")
        DB_HOST = env.str("DB_HOST")
        DB_PORT = env.str("DB_PORT")

        dump_file = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"

        # Dumpni olish uchun bash komandasi

        command = f"pg_dump -U {DB_USER} -h {DB_HOST} -p {DB_PORT} {DB_NAME} > {dump_file}"
        os.environ['PGPASSWORD'] = DB_PASSWORD
        # Komandani bajarish
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while executing command: {e}")
            send_msg_log(f"Central system backup\nError occurred while executing command: {e}")
            return

        # sending backup file
        if BackupDbBot.objects.all().count() > 0:
            token = BackupDbBot.objects.last().token
            channel_id = BackupDbBot.objects.last().channel_id
        else:
            token = "6567332198:AAHRaGT5xLJdsJbWkugqgSJHbPGi8Zr2_ZI"
            channel_id = -1002041724232

        send_to_telegram(token, channel_id, dump_file, f"All bots: > Backup file: {dump_file}")

        # delete backup file
        txt = f"Central system backup\ndelete dump database after send::\n"

        if os.path.exists(dump_file):
            os.remove(dump_file)
            txt += f"delete    = {dump_file}\n"
        else:
            txt += f"error delete = {dump_file}\n"

        send_msg_log(txt)
    except Exception as e:
        # all files finish with .sqlite3
        send_msg_log(f"Central system backup\nError occurred while executing command: {e}")


__all__ = ["backup_database"]
