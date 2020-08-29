class BotError(Exception):
    def __init__(self, user_message):
        self.user_message = user_message

    def __str__(self):
        return self.user_message


class UnexpectedBotError(BotError):
    """This should be raised from the causing error, with the cause explicitly passed in."""

    def __init__(self, cause):
        # TODO(jsteel): "Maintainer of this bot" should be configurable?
        super().__init__(
            "Oops! Something went wrong :( Either try again or contact the maintainer of this bot.\n" +
            f"`Unexpected exception: {type(cause)}, {cause}`")


def handle_unexpected_exceptions(func):
    async def wrapper(*args, **kw):
        try:
            return await func(*args, **kw)
        except BotError:
            raise
        except Exception as e:
            print(f"Unexpected exception: {type(e)}, {e}")
            raise UnexpectedBotError(e) from e

    return wrapper
