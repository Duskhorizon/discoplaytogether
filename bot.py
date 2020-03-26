from datetime import datetime, timedelta
import os
import django
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from django.utils import timezone

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


def delete_old_events():
    now = timezone.localtime(timezone.now())
    for event in Event.objects.all():
        if event.start_time < now:
            event.delete()
            print('skasowalem dziada')


async def check_for_participations():
    now = timezone.localtime(timezone.now())
    for participation in Participation.objects.all():
        if participation.notify is True and participation.notified is False:
            if participation.notify_time < now:
                participation.notified = True
                participation.save()
                time_dif = participation.event.start_time - now
                time_dif_to_min = divmod(time_dif.seconds,60)
                usertonotify = participation.player
                usertonotofifysocial = usertonotify.socialaccount_set.all()[0]
                print(usertonotofifysocial.uid)
                user_to_msg = bot.get_user(int(usertonotofifysocial.uid))
                print(user_to_msg)
                await user_to_msg.send('Hej niedługo gierka!')
                embed = discord.Embed(title="Powiadomienie o nadchodzącej grze", url="https://zapisywanko.tk/events/{}".format(participation.event.id), color=0x1f5bd7)
                embed.set_author(name="Discoplaytogether")
                embed.set_thumbnail(url="https://zapisywanko.tk/static/logo.png")
                embed.add_field(name="Gra:", value=participation.event.game.title, inline=False)
                embed.add_field(name="Serwer ", value=participation.event.server.name, inline=True)
                embed.add_field(name="Organizator :", value=participation.event.creator.username, inline=True)
                embed.add_field(name="Zaczyna się za minut:", value=format(time_dif_to_min[0]), inline=True)
                await user_to_msg.send(embed=embed)


class Check(commands.Cog):
    def __init__(self, bot):
        self.index = 0
        self.printer.start()
        self.bot = bot

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(seconds=10)
    async def printer(self):
        try:
            delete_old_events()
            await check_for_participations()
        except Exception as e:
            print(e)
            print(e.message)


bot.add_cog(Check(bot))
bot.run(token)
