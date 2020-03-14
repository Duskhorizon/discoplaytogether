import os
import django
from discord.ext import commands
from dotenv import load_dotenv

os.environ['DJANGO_SETTINGS_MODULE'] = 'discoplaytogether.settings'
django.setup()

from allauth.socialaccount.models import SocialAccount
from posts.models import *

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='&')


@bot.event
async def on_message(message):
    if message.guild is None and message.author != bot.user:
        if 'hi' in message.content:
            user_id = message.author.id
            user = bot.get_user(user_id)
            print(user_id)
            if verify_user(user_id):
                await user.send('Dzięki za rejestracje, powiązaliśmy cię z kontem na stronie')
                await user.send(
                    'Razem znajdujemy się na nastepujących serwerach {} - jak w przyszłości dołączysz do nowego '
                    'serwera na którym jest nasz bot, odezwij się do mnie ponownie'.format(check_for_common_guilds(
                        bot, user_id)))
            else:
                await user.send('Hej, zapraszamy na stronkę zapisywanko.tk w celu rejestracji, po jej zakończeniu '
                                'odezwij się do mnie proszę jeszcze raz')


def verify_user(user_id):
    for account in SocialAccount.objects.all():
        print(account.uid)
        print(type(user_id))
        print(type(account.uid))
        print(int(account.uid) == user_id)
        if int(account.uid) == user_id:
            account.user.verified = True
            account.user.save()
            return True
        else:
            return False


def check_for_common_guilds(bot, user_id):
    common_guilds = []
    for guild in bot.guilds:
        for member in guild.members:
            if user_id == member.id:
                dj_user = SocialAccount.objects.get(uid=str(user_id))
                dj_server, created = DiscoServer.objects.get_or_create(name=guild.name, uid=str(guild.id))
                dj_server.save()
                member = Membership(user=dj_user.user, server=dj_server, subbed=True)
                member.save()
                common_guilds.append(guild.name)
                return common_guilds


bot.run(token)
