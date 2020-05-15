Noodles discord bot
===================

.. image:: https://discordapp.com/api/guilds/705526724783505518/embed.png
   :target: https://discord.gg/Kzcr6pE
   :alt: Discord server invite

Discord bot made by DankDumpster#4806 (357918459058978816)

.. code:: sh

    git clone https://github.com/DankDumpster/Noodles

Requirements
------------

- Python >= 3.7
- `Discord.py <https://github.com/Rapptz/discord.py>`_
- `Praw <https://praw.readthedocs.io/en/latest/>`_
- Psuitl
- Numpy
- Pillow

Setup
-----
Create a secret.py file in utils/

.. code:: py
   
   # Reddit stuff
   client_id = ''
   client_secret = ''
   username = ''
   password = ''
   user_agent = ''
   # Basic stuff
   TOKEN = '' # Your bot token
   DATABASE = '' # Your postgresql url, you can set one up at https://www.elephantsql.com/
   repo = '' # Your forked repo for pull command
   
Roadmap
-------
- ☑ Add an level system
- ☑ Add an economy 
- ☐ Create levels with the PIL libary
- ☐ Smooth database management
- ☐ Documentation with flask or django
- ☐ Public release


