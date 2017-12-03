import telepot

from django.conf import settings


TELEGRAM_TOKEN = '485810747:AAFtvkMs7Sr45CwV9V0GbkLv09rsUO7RYn0'
bot = telepot.Bot(TELEGRAM_TOKEN)

#bot.remove_webhook()
WEBHOOK_URL_BASE = 'https://185.9.81.136:443'
WEBHOOK_URL_PATH = "/%s/" % (TELEGRAM_TOKEN)
WEBHOOK_SSL_CERT = '/home/user/cert/webhook_cert.pem'

# Ставим заново вебхук
bot.setWebhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))