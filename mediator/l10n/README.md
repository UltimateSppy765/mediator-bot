## Localization Folder
The `l10n` folder contains files that build a framework to allow for the bot to respond with multiple languages if needed.

## Languages Supported
*The languages will be in [Discord's locale format](https://discord.com/developers/docs/reference#locales).

Currently supported languages:
- English (en-GB, en-US)

## Sample for using l10n in the bot:
The l10n for a particular Python file can be split to a separate JSON file containing responses in the given format:

`file1.json`
```json
{
    "somecommand": {
        "response": {
            "en-US": "You input: {somearg}",
            "en-GB": "You have input: {somearg}"
        },
        "errorresponse": {
            "en-US": "What you entered is not an integer, please try again with an integer.",
            "en-GB": "What you've entered isn't an integer. Please try again with an integer."
        }
    }
}
```

And can be used in the Python file by reading the respective JSON:

`file1.py`
```py
import json

l10nfile = "l10n/file1.json"

with open(l10nfile, 'r') as file:
    l10ndata = json.load(file)

def somecommand(somearg: int):
    print(l10ndata['somecommand']['response']['en-GB'].format(somearg))

try:
    somecommand(int(input('Enter an integer.')))
except TypeError:
    print(l10ndata['somecommand']['errorresponse']['en-US'])
```

_The given localizations are just a sample, they are not meant to reflect their respective language in reality._ 
