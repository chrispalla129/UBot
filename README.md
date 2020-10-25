Note: This cannot be ran without a .env containing the Discord Token & Guild Name
Inspiration
We were inspired by having to take online classes and utilizing many different services such as Zoom. We wanted to see if we could implement a competitive all in one system on Discord.

What it does
It gives a professor extra tools when running a class through Discord. It provides features such as making quizzes, running office hours, and having useful shortcuts for the student.

How we built it
We built the project in PyCharm using the Discord.py plugin. A Discord bot can be created through Discord Developer, and from there it can be ran locally or on a server.

Challenges we ran into
One of the biggest challenges we ran into was reading through the documentation to find the more niche features. Discord.py went through an overhaul of it's API, called Discord Rewrite, about 1 year ago. This made any documentation from beyond that basically useless. We had to comb through a lot of official documentation to learn exactly how to use many of it's features.

Accomplishments that we're proud of
Our Office hours queue that allows students to get in line in a waiting room and allows the Professor / TA running office hours to call in the next student in the queue to a private voice chat using a command.

Our feature in our response system that allows a professor to get a CSV file of all student responses to every poll given on the server.

What we learned
This was a good experience in having to read documentation. We also learned throughout creating the project, that writing purposeful code that lends itself for testing makes the development process go much faster (and leaving many comments for when someone else looks at your functions).

What's next for UBot
The project most likely could benefit from more rigorous testing to ensure that it is completely stable.

Built With
discord.py
pycharm
python
