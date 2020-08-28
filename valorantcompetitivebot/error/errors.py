class BotError(Exception):
    def __init__(self, user_message):
        self.user_message = user_message

    def __str__(self):
        return self.user_message
