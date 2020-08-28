# ValorantCompetitiveBot

ValorantCompetitiveBot is a Reddit bot used to assist subreddit moderation.

It is also responsible for updating a live sidebar with top streams and upcoming competitive matches.

The aim of this bot is to make it reusable for any subreddit with similar requirements via config.

## Installation

```bash
pip install -r requirements.txt
```

Create a venv
```bash
pip install -e .
```

## Config

Copy the `config/config.yaml.example` file to `config/config.yaml` and then input the fields as required.

## Running

Running with Python 3, simply run `python valorantcompetitivebot/main.py`

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)