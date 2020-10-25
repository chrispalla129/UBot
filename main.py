# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import discord
import os
import OfficeHours
import ResponseSystem
from discord.utils import get
from discord import Message
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, MissingPermissions, Context
from dotenv import load_dotenv

global student
global ta
global professor

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# bot init


global class_syllabus
print(discord.version_info)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot('$', intents=intents)


@bot.event
async def on_member_join(member: discord.Member):
    print("Here")
    await member.add_roles(student)
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my class! Here is a link to the syllabus ' + class_syllabus
    )


@bot.command(name="set_ta", help="Usage: $set_ta @targ")
@commands.has_role("Professor")
async def set_ta(ctx, target: discord.Member):
    if get(target.roles, name="Student"):
        await target.remove_roles(student)
        await target.add_roles(ta)
    elif get(target.roles, name="TA"):
        await ctx.send(f"{target.display_name} is already a TA.")
    else:
        await ctx.send(f"{target.display_name} isn't a student.")


@bot.command(name="define_syllabus", help="Allows you to set the syllabus. Usage is $define_syllabus <file link>")
@commands.has_role("Professor")
async def define_syllabus(ctx, syllabus):
    try:
        global class_syllabus
        class_syllabus = ctx.message.content
        await ctx.send(syllabus + 'has been set ')
    except MissingPermissions:
        await ctx.send(f"{ctx.message.author.mention} You're not allowed to do that!")


@bot.command(name='syllabus', help='returns a link to the syllabus')
async def syllabus(ctx):
    if class_syllabus != "not yet defined":
        await ctx.send(f"{ctx.message.author.mention} here is the syllabus " + class_syllabus)
    else:
        await ctx.send(f"The syllabus has not been set yet, please ask the professor to rectify this.")


@bot.command(name='Initialize', help='Sets up the server for class. Please run this before anything else.')
async def begin(ctx: Context):
    guild: discord.Guild = ctx.message.guild
    studentPerms = discord.Permissions(add_reactions=True, stream=True, read_messages=True, view_channel=True,
                                       send_messages=True, embed_links=True, read_message_history=True, connect=True,
                                       speak=True)
    if not get(guild.roles, name="Professor"):
        await guild.create_role(name="Professor", permissions=discord.Permissions.all())
    if not get(guild.roles, name="TA"):
        await guild.create_role(name="TA", permissions=discord.Permissions.all_channel())
    if not get(guild.roles, name="Student"):
        await guild.create_role(name="Student", permissions=studentPerms)

    global class_syllabus
    class_syllabus = "not yet defined"

    global student
    global ta
    global professor
    student = get(guild.roles, name="Student")
    ta = get(guild.roles, name="TA")
    professor = get(guild.roles, name="Professor")

    for channel in guild.channels:
        await channel.delete()
    for category in guild.categories:
        if category is not None:
            await category.delete()

    await guild.create_category("Class")
    await guild.create_category("Office Hours")
    await guild.create_category("General")

    for category in guild.categories:
        if category.name == "Class":
            await category.create_voice_channel("Class Lecture")
            await category.create_text_channel("Class Discussion")
            #await get(guild.voice_channels, name="Class Lecture").set_permissions(student, speak=False)
        elif category.name == "Office Hours":
            await category.create_voice_channel("Office Hours Discussion 1")
            await category.create_voice_channel("Office Hours Discussion 2")
            await category.create_voice_channel("Office Hours Waiting Room")
            #await get(category.voice_channels, name="Office Hours Waiting Room").set_permissions(student, speak=False)
            await category.create_text_channel("Office Hours Q&A")
        elif category.name == "General":
            await category.create_voice_channel("Student Discussion 1")
            await category.create_voice_channel("Student Discussion 2")
            await category.create_voice_channel("Student Discussion 3")
            await category.create_text_channel("General Chat")
            await category.create_text_channel("Off-Topic")

    for member in guild.members:
        await member.add_roles(professor)
        if not member.bot:
            await member.create_dm()
            await member.dm_channel.send(
                f"Hello {member.name}, you have been set as a teacher for this class, and any future users will be"
                f" set as students. Use $help for all of the commands available."
            )


bot.add_cog(OfficeHours.office_hours())
bot.add_cog(ResponseSystem.response_system())
bot.run(token)
