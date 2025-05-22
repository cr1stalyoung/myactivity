<p align="center">
      <img src="https://i.ibb.co/QmfBQtC/myactivity.png">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/follow-cr1stalyoung-white?style=flat-square&color=white" alt="follow me">
  <img src="https://img.shields.io/badge/python-3.12-white?style=flat-square&color=green" alt="python_version">
  <img src="https://img.shields.io/badge/disnake-2.9.2-white?style=flat-square&color=blue" alt="python_version">
  <img src="https://img.shields.io/badge/pillow-10.3.0-white?style=flat-square&color=red" alt="python_version">
</p>

> [!IMPORTANT]  
> **This bot was designed to be used across multiple servers simultaneously. If you only need it for use on a single server, you'll need to use the bot's code as a base and adapt it for single-server operation. The bot was developed using the technologies and versions listed above**

> [!WARNING]  
> **To run the bot you need to create the necessary tables, columns, values, and relationships based on the model files located in app/models**

## Installation
1. Clone this repo into folder ;
2. Install dependencies: `pip install -r requirements.txt` ;
3. Go to [Google Drive](https://drive.google.com/drive/folders/1_DDrPEOE7yb1neX7TOLmA6U1idFS2Esw?usp=drive_link) and download animation files ;
4. Place the files in [cases](https://github.com/cr1stalyoung/tracking-activity-discord-bot/tree/main/resources/cases) ;
5. Add your bot `API_TOKEN` and connection to PostgreSQL `DATABASE_URL` in [settings.py](https://github.com/cr1stalyoung/tracking-activity-discord-bot/blob/main/settings.py) .

<hr style="border: 3px solid #000;">

### General Information

<p align="center">
      <img src="https://i.ibb.co/PYxfQ6X/banner.png">
</p>

**MyActivity** is a themed Discord bot for Call of Duty that tracks server activity and enables competition with other servers or members using a ranking system. Engage in text or voice chat to earn SR ranking points and CP coins that allows you to unlock chests and enhance your profile.

**Earning Coins:**
+  You earn `1` coin for every minute spent on voice channels.
+  You earn `50` coins for every new level.

**Bot Commands:**
+ `/me` - View information about your own or someone else's profile.
+ `/leaders` - Show server leaderboard.
+ `/top50` - Show world ranking leaderboard.
+ `/help` - Information about the bot or help

<hr style="border: 3px solid #000;">

### Rating System
<p align="center">
      <img src="https://i.ibb.co/b5nm63m/ranking.png">
</p>

Get ready to dive into a brand new rating activity system in voice channels. Progress through divisions earning SR points for activity. You earn 4 SR points for every minute spent in voice channels. For every one hour of absence in a voice channel, you receive a penalty of points depending on your division.

**Division:**
+ Bronze `0 - 899` SR
+ Silver `900 - 2099` SR
+ Gold `2100 - 3599` SR
+ Platinum `3600 - 5399` SR
+ Diamond `5400 - 7499` SR
+ Crimson `7500 - 9999` SR
+ Iridescent `10000+` SR
+ World Top 50 `10000+` SR

**Division penalties per hour:**
+ Bronze `(0)` SR
+ Silver `(-3)` SR
+ Gold `(-10)` SR
+ Platinum `(-12)` SR
+ Diamond `(-15)` SR
+ Crimson `(-18)` SR
+ Iridescent `(-25)` SR
+ World Top 50 `(-25 to -150)` SR

<hr style="border: 3px solid #000;">


### Leveling

You can progress through the bot's level system. Starting from the first level and ending with the maximum 300th level. For certain levels you move to a new prestige, which gives you a significant increase in CP coins.

<p align="center">
      <img src="https://i.ibb.co/1ZrrQkB/leveling.png">
</p>

<hr style="border: 3px solid #000;">

### Open Cases

The bot has a function of opening cases from which you can get items to decorate your profile, both personal and public. 

**Item Drop Rates:**
+ Common item - `~53%`;
+ Uncommon item - `~35%`;
+ Mythical item - `~10%`;
+ Ancient item - `~0.25%`;
+ Ultra Rare item - `~0.01%`.

<p align="center">
      <img src="https://i.ibb.co/DYYsG12/immortal.gif">
</p>

<hr style="border: 3px solid #000;">
