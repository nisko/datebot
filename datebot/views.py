from django.shortcuts import render
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.backends.sqlite3 import base

from .dbworker import *
import json
import telepot
import re


TelegramBot = telepot.Bot(settings.TELEGRAM_TOKEN)


def _display_help(chat_id, text):
    return render_to_string('help.md')

def _add_date(chat_id, text):
    if len(text.split()) < 2:
        return "please give date in xx.yy format"
    if len(text.split()) > 2:
        description = ' '.join(text.split()[2:])
    else :
        description = ''

    date = text.split()[1]
    pattern = re.compile("^([0-9.]+)+$")

    if (pattern.match(date)):
        if add_date(date.split('.')[0], date.split('.')[1], description, chat_id):
            return "date added"
        else:
            return "error"
    else:
        return "please give date in xx.yy format"

def _get_all_date(chat_id,text):
    return get_all_date(chat_id)

def _get_date_by_month(chat_id,text):
    pattern = re.compile("^([0-9]+)+$")
    if len(text.split()) < 2:
        return "give me month number, bro"
    else:
        if (pattern.match(text.split()[1])):
            return get_date_by_month(text.split()[1], chat_id)
        else:
            return "give me month number, bro"

# Create your views here.
class CommandReceiveView(View):
    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_TOKEN:
            return HttpResponseForbidden('Invalid token')

        commands = {
            '/start': _display_help,
            '/adddate': _add_date,
            '/getalldate': _get_all_date,
            '/getdatebymonth': _get_date_by_month,
        }

        raw = request.body.decode('utf-8')

        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:

            chat_id = payload['message']['chat']['id']
            cmd = payload['message'].get('text')

            func = commands.get(cmd.split()[0].lower())
            if func:
                TelegramBot.sendMessage(chat_id, func(chat_id, cmd), parse_mode='Markdown')
            else:
                TelegramBot.sendMessage(chat_id, 'I do not understand you, Bro!')

        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)
