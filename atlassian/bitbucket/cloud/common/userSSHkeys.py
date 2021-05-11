# coding=utf-8
import logging

logger = logging.getLogger(__name__)
from requests import HTTPError

from ..base import BitbucketCloudBase


class SSHkeys(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(SSHkeys, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        return SSHkey(data, **self._new_session_args)

    def each(self, q=None, sort=None):
        """
        Returns the user"s SSH keys.
        :param q: string: Query string to narrow down the response.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :return: A generator for the SSHKey objects
        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/deploy-keys
        """
        params = {}
        if sort is not None:
            params["sort"] = sort
        if q is not None:
            params["q"] = q
        for ssh_key in self._get_paged(None, params=params):
            yield self.__get_object(ssh_key)
        return

    def add(self, label, key):
        """
        creates or update the ssh keys for this user.
        :param label: string: The ssh key label
        :param key:   string: The ssh key RSA key
        :return: The requested SSH-KEY object, None if not a there are no keys
        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/users/%7Bselected_user%7D/ssh-keys#post


        """

        data = {"label": label, "key": key}
        return self.__get_object(self.post(None, data=data))

    def update(self, key_id, label=None, comment=None):
        # WIP update not working
        # TODO: docu string
        ssh_key = self.get(key_id)
        data = {}
        # TODO: do data manage if no values for label and comment
        data = {}
        data["key"] = ssh_key.key
        data["comment"] = comment
        data["label"] = label
        logger.warning("WIP     -----")
        logger.debug(f"key_id:{key_id} \n data:{data}")

        return self.__get_object(self.put(key_id, data=data))

    def remove(self, id):
        """
        delete a ssh keys against this user.
        :param id: string: The ssh key id
        :return:
        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/users/%7Bselected_user%7D/ssh-keys/%7Bkey_id%7D#delete
        """
        return self.delete(id)

    def get(self, key_id):
        """
        Returns the ssh keys for this user.
        :param key_id: string: The requested ssh key
        :return: The requested ssh-key object, None if not a there are no keys
        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/users/%7Bselected_user%7D/ssh-keys/%7Bkey_id%7D#get
        """
        ssh_key = None
        try:
            ssh_key = self.__get_object(super(SSHkeys, self).get(key_id))
        except HTTPError as e:
            # A 404 indicates that the specified id is not in deploy keys.
            if not e.response.status_code == 404:
                # Rethrow the exception
                raise

        return ssh_key


class SSHkey(BitbucketCloudBase):
    def __init__(self, data, *args, **kwargs):
        super(SSHkey, self).__init__(None, *args, data=data, expected_type="ssh_key", **kwargs)

    @property
    def label(self):
        return str(self.get_data("label"))

    @property
    def key(self):
        return self.get_data("key")

    @property
    def key_id(self):
        return self.get_data("uuid")
