import discord
import os

## Discord
# Guild ID
guildid = os.environ.get("GUILDID")
# Token
token = os.environ.get("TOKEN")

bot = discord.Bot(intents = discord.Intents.all())

@bot.slash_command(guild_ids = [guildid], pass_context=True)
async def role(ctx:discord.ApplicationContext):
    member = ctx.author
    role = discord.utils.get(ctx.guild.roles, name="dev")
    await member.add_roles(role)



@bot.slash_command(guild_ids = [guildid])
async def reac(ctx:discord.ApplicationContext):
    global message_id
    role = discord.utils.get(ctx.guild.roles, name="dev")
    msg = await ctx.send(f"このメッセージに👍でロール {role.mention} を取得")
    message_id = msg.id
    print(message_id)
    await msg.add_reaction("👍")

@bot.event
async def on_raw_reaction_add(payload):
    global message_id
    print(message_id)
    channel = bot.get_channel(payload.channel_id)
    if payload.user_id == bot.user.id:
        return
    if payload.message_id == message_id:
        print("Reaction added")
        checked_emoji = payload.emoji
        print(checked_emoji)
        member = payload.member
        guild = bot.get_guild(payload.guild_id)
        if str(checked_emoji) == "👍":
            print("Role added")
            role = discord.utils.get(guild.roles, name="dev")
            await member.add_roles(role)
            await channel.send(f"{member.mention} {role.mention} を付与しました", delete_after=5)

bot.run(token)