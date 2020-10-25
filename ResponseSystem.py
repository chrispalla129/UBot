import discord
from discord.ext import commands
from discord.utils import get
import csv
import os


# command prompt = $Poll: <Title> [Option1, Option2, Option3, etc]
class response_system(commands.Cog):
    bot = commands.Bot('$')

    def __init__(self):
        self.pollList = []
        self.optionDict = {
            1: "\N{REGIONAL INDICATOR SYMBOL LETTER A}",
            2: "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
            3: "\N{REGIONAL INDICATOR SYMBOL LETTER C}",
            4: "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
            5: "\N{REGIONAL INDICATOR SYMBOL LETTER E}",
            6: "\N{REGIONAL INDICATOR SYMBOL LETTER F}",
            7: "\N{REGIONAL INDICATOR SYMBOL LETTER G}",
            8: "\N{REGIONAL INDICATOR SYMBOL LETTER H}",
            9: "\N{REGIONAL INDICATOR SYMBOL LETTER I}",
            10: "\N{REGIONAL INDICATOR SYMBOL LETTER J}",
            11: "\N{REGIONAL INDICATOR SYMBOL LETTER K}",
            12: "\N{REGIONAL INDICATOR SYMBOL LETTER L}",
            13: "\N{REGIONAL INDICATOR SYMBOL LETTER M}",
            14: "\N{REGIONAL INDICATOR SYMBOL LETTER N}",
            15: "\N{REGIONAL INDICATOR SYMBOL LETTER O}",
            16: "\N{REGIONAL INDICATOR SYMBOL LETTER P}",
            17: "\N{REGIONAL INDICATOR SYMBOL LETTER Q}",
            18: "\N{REGIONAL INDICATOR SYMBOL LETTER R}",
            19: "\N{REGIONAL INDICATOR SYMBOL LETTER S}",
            20: "\N{REGIONAL INDICATOR SYMBOL LETTER T}",
            21: "\N{REGIONAL INDICATOR SYMBOL LETTER U}",
            22: "\N{REGIONAL INDICATOR SYMBOL LETTER V}",
            23: "\N{REGIONAL INDICATOR SYMBOL LETTER W}",
            24: "\N{REGIONAL INDICATOR SYMBOL LETTER X}",
            25: "\N{REGIONAL INDICATOR SYMBOL LETTER Y}",
            26: "\N{REGIONAL INDICATOR SYMBOL LETTER Z}"
        }

    # will grab title, from message
    def set_title(self, message):

        titleStart = message.find("<") + 1
        titleEnd = message.find(">")
        return message[titleStart:titleEnd]

    # will grab options from message
    def set_options(self, message):
        listStart = message.find("[") + 1
        listEnd = message.find("]")
        optionList = message[listStart:listEnd].split(',')
        return optionList

    @bot.command(name="Poll", help="Allows you to create a multiple choice poll. Usage: $Poll <Question> [Choice 1, "
                                   "Choice 2, ..., etc]")
    @commands.has_any_role("Professor", "TA")
    async def command_listener(self, ctx):
        # Poll will be initiated when message starts with $Poll:
        input = ctx.message.clean_content  # grabs message
        if input.find("<") == -1 or input.find(">") == -1:
            # Ensure title is given in desired format
            await ctx.send("Poll requires valid title: <Question>")
            return
        title = self.set_title(input)
        if input.find("[") == -1 or input.find("]") == -1:
            # Ensure options are given in desired list format
            await ctx.send("Poll requires valid response options: [Choice 1, Choice 2, ... ,etc]")
            return
        options = self.set_options(input)

        if options:  # Checks that response list isn't empty
            if len(options) <= 26:
                poll = ""
                optionNum = 0
                for response in options:
                    optionNum += 1
                    # the content of the Poll (the question and the options)
                    poll = poll + "\n\n" + self.optionDict[optionNum] + " " + response
            else:
                await ctx.send("Polls only support 26 different")

            # Sets up a discord embed to house the poll
            pollEmbed = discord.Embed(title=title, description=poll, colour=0x005bbb)
            sendPoll = await ctx.send(embed=pollEmbed)

            optionNum = 0
            for response in options:
                optionNum += 1
                await sendPoll.add_reaction(self.optionDict[optionNum])

            self.pollList.append((title, options, sendPoll.id))

    def Diff(self, li1, li2):
        return list(list(set(li1) - set(li2)) + list(set(li2) - set(li1)))

    # {Poll Title: title, Option A: [List], Option B: [List 2], ...., etc}
    # {Student: [Question, Answer]}

    @bot.command(name="Close_Polls", help="Creates a CSV file that can be accessed in spreadsheet software of all student responses on every poll given on the server")
    @commands.has_any_role("Professor", "TA")
    async def capture_polls(self, ctx):
        if not self.pollList:
            await ctx.send("No polls have been ran yet.")
            return
        rev_map = {v: k for k, v in self.optionDict.items()}
        key = []
        data = {}
        # Getting all users under the tag students
        allStudents = get(ctx.message.guild.roles, name="Student").members
        # Creating an index in the list for each student, creates a dictionary of the student's name to a list of
        # their answers
        for student in allStudents: data[student.name] = []
        # Loops through all questions currently in poll list
        for title, options, identity in self.pollList:
            q = await ctx.fetch_message(identity)
            key.append(title)  # Appends the question title to a separate list as a key
            for reaction in q.reactions:  # Loops through each reaction (or choice) for said question
                users = await reaction.users().flatten()  # Get's all users who chose that answer
                for student in users:
                    if not student.bot: data[student.name].append(rev_map[reaction.emoji])  # Loops through students

                # Removes the students who picked this choice from allStudents, so in the end any students who didn't
                # pick an answer are left
                allStudents = self.Diff(allStudents, users)

            # Runs through the student's who didn't answer, and appends an empty choice, because we have to keep the
            # list consistent
            for student in allStudents:
                if not student.bot: data[student.name].append("")
            # Reset this variable to contain all students at the start of the for loop
            allStudents = get(ctx.message.guild.roles, name="Student").members
        self.pollList.clear()

        with open("output.csv", "w") as f_output:
            csv_output = csv.writer(f_output)
            key.insert(0, "Students:")
            csv_output.writerow(key)

            for student, answers in data.items():
                final = [student] + answers
                csv_output.writerow(final)

        professor = ctx.message.author
        await professor.create_dm()
        await professor.dm_channel.send(
            f"Here are the results of your questions: "
        )
        await professor.dm_channel.send(files=[discord.File("output.csv")])

