import logging

logger = logging.getLogger(__name__)
from ..base import BitbucketCloudBase


class UsersBase(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(UsersBase, self).__init__(url, *args, **kwargs)

    def _get_object(self, data):
        logger.debug(f"UserBase _get_object data:{data}")
        return User(None, data=data, **self._new_session_args)


class User(BitbucketCloudBase):
    # def __init__(self, url, data, *args, **kwargs):
    #     super(User, self).__init__(url, *args, data=data, expected_type="user", **kwargs)
    def __init__(self, url, *args, **kwargs):
        super(User, self).__init__(url, *args, expected_type="user", **kwargs)

    @property
    def display_name(self):
        return str(self.get_data("display_name"))

    @property
    def nickname(self):
        return self.get_data("nickname")

    @property
    def account_id(self):
        return self.get_data("account_id")

    @property
    def uuid(self):
        return self.get_data("uuid")


class CurrentUser(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        logger.debug(f"CurrentUser - init,\n url: {url}\n args: {args}\n kwargs:{kwargs} ")
        super(CurrentUser, self).__init__(url, *args, **kwargs)
        # super(CurrentUser, self).get("")

    def __get_object(self, data):
        return User(None, data=data, **self._new_session_args)

    def lookup(self):
        """
        Returns the issue with the ID in this repository.

        :param id: string: The requested issue ID

        :return: The requested Issue objects

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/issues/%7Bissue_id%7D#get
        """
        return self.__get_object(super(CurrentUser, self).get(""))

    @property
    def display_name(self):
        return str(self.get_data("display_name"))

    @property
    def nickname(self):
        return self.get_data("nickname")

    @property
    def account_id(self):
        return self.get_data("account_id")

    @property
    def uuid(self):
        return self.get_data("uuid")


class Users(UsersBase):
    def __init__(self, url, *args, **kwargs):
        super(Users, self).__init__(url, *args, **kwargs)

    # def _get_object(self, data):
    #     return User(data, **self._new_session_args)

    def get(self, user, by="account_id"):
        """
        Returns the requested user

        :param user: string: The requested user.
        :param by: string: How to interprate user, can be 'account_id' '.

        :return: The requested User object

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/users/%7Bselected_user%7D#get
        """
        if by == "account_id":
            return self._get_object(super(Users, self).get(user))
        # elif by == "name":
        #     for r in self.each():
        #         if r.name == user:
        #             return r
        else:
            ValueError("Unknown value '{}' for argument [by], expected 'account_id' ".format(by))

        raise Exception("Unknown user {} '{}'".format(by, user))