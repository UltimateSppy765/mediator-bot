# Mediator - The Bot

A moderation Discord made with following goals in mind:
- Fully leverage Discord's interaction API
- Utilise in built moderation features provided by Discord for seamless moderation
- Attempts to automate chat moderation using ML (I will try to incorporate this using Google's [Perspective Comment Analyser API](https://www.perspectiveapi.com/))
- Clean user interface (at least my best attempts)
- Low latency responses
- Localization support (Not yet decided tbh, will just be building the framework for this)
- And maybe more stuff... ✨

---
## How to use the bot:
Since the bot is primarily interaction based, you can use the bot using Slash Commands!
![Screenshot_20220305_150931](https://user-images.githubusercontent.com/73820738/156877714-3d099a64-5920-4b03-a22a-4849dae8a25a.jpg)

You can also use the bot through context menus. (**Desktop Only** as of now)
![Screenshot_2022_0305_151524](https://user-images.githubusercontent.com/73820738/156877931-41200774-447e-4adc-8557-1d769323d6e7.jpg)

## What features does it offer?
- Basic Moderation features
- Chat Analyser (Using [Perspective Comment Analyser API](https://www.perspectiveapi.com/))
- Neat interface
- Fast bot
- Default Emojis (come on, they are not that bad)

## Why should I choose this bot?
You shouldn't. Because you cannot invite it. You can fork the code however and customise it to your own needs (except for the chat analyser part since it needs an API key).

**Keep in mind that the slash commands and context menus are not automatically registered by this code, I've pre registered them for my bot instance over HTTP and if you need any help with registering application commands, please visit the [#application-commands](https://discord.com/channels/613425648685547541/788586647142793246) channel in [Discord Developers Server](https://discord.gg/discord-developers).

## Anything else?
Nothing, I just felt it will be nice to have a README so I added one and it doesn't make a difference so as to whether you read this or not.
Have fun and touch some grass occasionally. Bye! 👋
