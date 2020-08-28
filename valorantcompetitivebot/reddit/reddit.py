import asyncpraw
import asyncpraw.exceptions

from valorantcompetitivebot.config.config import RedditConfig
from valorantcompetitivebot.error.errors import BotError


class Reddit:
    """
    Wraps the praw Reddit instance with appropriate helper methods to perform required actions.
    """

    def __init__(self, config: RedditConfig):
        # TODO(jsteel): user_agent should be configurable to at least some degree?
        # TODO(jsteel): Version number should be extracted
        self.user_agent = 'script:nz.co.jacksteel.valorantcompetitivebot:v0.1 (by /u/iPlain)'
        self.config = config
        self._r = self._get_praw_instance()

    def _get_praw_instance(self):
        r = asyncpraw.Reddit(user_agent=self.user_agent,
                             client_id=self.config.client_id,
                             client_secret=self.config.client_secret,
                             username=self.config.username,
                             password=self.config.password)
        return r

    async def sticky_post(self, post_url):
        submission = await self._get_post_from_url(post_url)
        # TODO(jsteel): Do we want to ensure only certain users posts can be stickied?
        try:
            await submission.mod.sticky(state=True, bottom=True)
        except Exception as e:
            raise InternalServerError from e

    async def unsticky_post(self, post_url):
        submission = await self._get_post_from_url(post_url)
        # TODO(jsteel): Do we want to ensure only certain users posts can be un-stickied?
        try:
            await submission.mod.sticky(state=False)
        except Exception as e:
            raise InternalServerError from e

    async def _get_post_from_url(self, post_url: str) -> asyncpraw.reddit.Submission:
        try:
            submission = await self._r.submission(url=post_url)
        except asyncpraw.exceptions.ClientException as e:
            raise RedditError(f"Something went wrong:\n{e}")
        except Exception as e:
            # TODO(jsteel): properly log
            print(f"{type(e)}: {e}")
            raise InternalServerError from e
        if submission.subreddit.display_name.lower() != self.config.subreddit.lower():
            raise IncorrectSubredditError(submission.subreddit.display_name)
        return submission


class RedditError(BotError):
    pass


class PostNotFoundError(RedditError):
    def __init__(self):
        super().__init__("That post could not be found")


class IncorrectSubredditError(RedditError):
    def __init__(self, subreddit_found):
        super().__init__(f"That post is in /r/{subreddit_found}!")


class UnauthorizedUserError(RedditError):
    def __init__(self, username):
        super().__init__(f"Posts from /u/{username} cannot be stickied!")


class InternalServerError(RedditError):
    """Should raise this from the causing error."""

    def __init__(self):
        # TODO(jsteel): "Maintainer of this bot" should be configurable?
        super().__init__("Oops! Something went wrong :( Either try again or contact the maintainer of this bot")
