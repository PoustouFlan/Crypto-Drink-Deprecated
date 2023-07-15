## CryptoDrink

**CryptoDrink** is a Discord bot which implements a local
scoreboard for [https://cryptohack.org/](CryptoHack).

 - Announces when a server member solves a challenge
 - Displays statistics about a CryptoHack user
 - Local scoreboard for your server
 - List who solved a challenge in your server

## Installation

First, you need to [https://discordpy.readthedocs.io/en/stable/discord.html](
create your own Discord bot)
The bot will need permissions to read messages, send messages and include
embeds.
It will also need the *Message Intent*.


Clone the repository using git
```bash
git clone https://github.com/PoustouFlan/Crypto-Drink.git
cd Crypto-Drink
```

Then, complete the file `configuration.yaml`:
```yaml
token:      "Your.Bot.Token-Here"
guild_id:   123456789012345678
channel_id: 1234567890123456789
locale:     "en"
```
 - `token` should be your Discord Bot token
 - `guild_id` should be the `id` of your Discord server
 - `channel_id` should be the id of the channel where the flags are announced
 - `locale` should be your prefered language.

### NixOS

You can simply run the bot using:
```bash
nix-shell --run make
```

### Non NixOS

You need to install the necessary Python packages using pip.
Assuming you have `python3` and `pip` installed, you can run
```bash
pip install -r requirements.txt
```
to install the necessary packages, then run
```bash
make
```
to start the bot.
