import asyncpraw
import asyncpraw.exceptions
import asyncprawcore.exceptions

from valorantcompetitivebot.config.config import RedditConfig
from valorantcompetitivebot.error.errors import BotError, handle_unexpected_exceptions


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

    @handle_unexpected_exceptions
    async def sticky_post(self, post_url):
        submission = await self._get_post_from_url(post_url)
        # TODO(jsteel): Do we want to ensure only certain users posts can be stickied?
        await submission.mod.sticky(state=True, bottom=True)

    @handle_unexpected_exceptions
    async def unsticky_post(self, post_url):
        submission = await self._get_post_from_url(post_url)
        # TODO(jsteel): Do we want to ensure only certain users posts can be un-stickied?
        await submission.mod.sticky(state=False)

    async def _get_post_from_url(self, post_url: str) -> asyncpraw.reddit.Submission:
        try:
            submission = await self._r.submission(url=post_url)
        except asyncpraw.exceptions.ClientException as e:
            raise RedditError(f"Something went wrong:\n{e}")
        except asyncprawcore.exceptions.NotFound:
            raise PostNotFoundError
        if submission.subreddit.display_name.lower() != self.config.subreddit.lower():
            raise IncorrectSubredditError(submission.subreddit.display_name)
        return submission


class RedditError(BotError):
    pass


class PostNotFoundError(RedditError):
    def __init__(self):
        super().__init__("That post could not be found :(")


class IncorrectSubredditError(RedditError):
    def __init__(self, subreddit_found):
        super().__init__(f"That post is in /r/{subreddit_found}!")


class UnauthorizedUserError(RedditError):
    def __init__(self, username):
        super().__init__(f"Posts from /u/{username} cannot be stickied!")
