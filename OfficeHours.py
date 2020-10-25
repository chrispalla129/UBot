import discord
import os
from discord.ext import commands
from queue import Queue
from discord.ext.commands import MissingAnyRole, CheckFailure


class office_hours(commands.Cog):
    bot = commands.Bot('$')

    def __init__(self):
        self.q = Queue()
        self.started = False

    # command to enqueue everyone waiting for office hours
    @bot.command(name='start_OH', help="Initializes a queue with all of the people in the Office Hours Wait Room")
    @commands.has_any_role("TA", "Professor")
    async def on_start(self, ctx):
        if ctx.message.author.voice is None:
            await ctx.send(f"{ctx.message.author.mention} Join a call to designate an office")
            return
        # check if OH already initialized
        if self.started:
            await ctx.send("Office hours have already begun")
            return

        # initialize OH and OH queue
        self.started = True
        await ctx.send("Office hours are starting! Join Office Hours Waiting Room and a TA will be with you")
        # has to be looked up in a for loop bc discord API is kinda dumb
        for channel in ctx.message.guild.voice_channels:
            if channel.name == "Office Hours Waiting Room":
                for student in channel.members:
                    self.q.put(student)

    @bot.command(name='next', help="sends the next person in the Queue to whichever TA called for the next student")
    @commands.has_any_role("TA", "Professor")
    async def get_next(self, ctx):
        try:
            if self.q:
                student = self.q.get()
                if student.voice.channel.name == "Office Hours Waiting Room":
                    await student.edit(voice_channel=ctx.message.author.voice.channel)
            else:
                await ctx.send("There are no students left in the queue")
        except discord.ext.commands.errors.MissingRole:
            ctx.send(f"{ctx.message.author.mention} You don't host Office Hours")

    @bot.command(name='join_line', help="put yourself at the end of the Queue")
    async def enqueue(self, ctx):
        if self.started:
            self.q.put(ctx.message.author)
        else:
            await ctx.send("Office hours aren't going right now")

    @bot.command(name='end_OH', help="Run this at the end of Office hours to empty the Queue")
    @commands.has_any_role("TA", "Professor")
    async def end(self, ctx):
        try:
            if self.started:
                self.started = False
                self.q = Queue()
                await ctx.send("Office hours are over")
            else:
                await ctx.send("Office hours were not going")
        except discord.ext.commands.errors.MissingRole:
            ctx.send(f"{ctx.message.author.mention} You don't host Office Hours")

    @on_start.error
    async def start_error(error, ctx):
        if isinstance(error, CheckFailure):
            await ctx.send("Looks like you don't have the perm.")
