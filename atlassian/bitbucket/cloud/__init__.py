# coding=utf-8

from .base import BitbucketCloudBase
from .workspaces import Workspaces
from .repositories import Repositories
from .common.users import CurrentUser
from .common.users import Users


class Cloud(BitbucketCloudBase):
    def __init__(self, url="https://api.bitbucket.org/", *args, **kwargs):
        kwargs["cloud"] = True
        kwargs["api_root"] = None
        kwargs["api_version"] = "2.0"
        url = url.strip("/") + "/{}".format(kwargs["api_version"])
        super(Cloud, self).__init__(url, *args, **kwargs)
        self.__workspaces = Workspaces("{}/workspaces".format(self.url), **self._new_session_args)
        self.__repositories = Repositories("{}/repositories".format(self.url), **self._new_session_args)
        self.__user = CurrentUser(
            "{}/user".format(self.url), {"type": "user"}, **self._new_session_args
        )  # set data to None ?
        self.__users = Users("{}/users".format(self.url), **self._new_session_args)

    @property
    def workspaces(self):
        return self.__workspaces

    @property
    def repositories(self):
        return self.__repositories

    @property
    def user(self):
        return self.__user

    @property
    def users(self):
        return self.__users