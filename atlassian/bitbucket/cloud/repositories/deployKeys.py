# coding=utf-8
import logging

logger = logging.getLogger(__name__)
from requests import HTTPError

from ..base import BitbucketCloudBase


class DeployKeys(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(DeployKeys, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        return DeployKey(data, **self._new_session_args)

    def each(self, q=None, sort=None):
        """
        Returns the repository"s deploy keys.
        :param q: string: Query string to narrow down the response.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :return: A generator for the DeployKeys objects
        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/deploy-keys
        """
        params = {}
        if sort is not None:
            params["sort"] = sort
        if q is not None:
            params["q"] = q
        for deploy_key in self._get_paged(None, params=params):
            yield self.__get_object(deploy_key)
        return

    def add(self, label, key):
        """
        creates or update the deploy keys in this repository.
        :param label: string: The deploy key label
        :param key:   string: The deploy key RSA key
        :return: The requested DeployKey object, None if not a there are no keys
        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/deploy-keys/%7Bkey_id%7D#put

        https://api.bitbucket.org/2.0/repositories/mleu/test/deploy-keys/1234 -d \
        '{
            "label": "newlabel",
            "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAK/b1cHHDr/TEV1JGQl+WjCwStKG6Bhrv0rFpEsYlyTBm1fzN0VOJJYn4ZOPCPJwqse6fGbXntEs+BbXiptR+++HycVgl65TMR0b5ul5AgwrVdZdT7qjCOCgaSV74/9xlHDK8oqgGnfA7ZoBBU+qpVyaloSjBdJfLtPY/xqj4yHnXKYzrtn/uFc4Kp9Tb7PUg9Io3qohSTGJGVHnsVblq/rToJG7L5xIo0OxK0SJSQ5vuId93ZuFZrCNMXj8JDHZeSEtjJzpRCBEXHxpOPhAcbm4MzULgkFHhAVgp4JbkrT99/wpvZ7r9AdkTg7HGqL3rlaDrEcWfL7Lu6TnhBdq5 newcomment",
        }'


        """

        data = {"label": label, "key": key}
        return self.__get_object(self.post(None, data=data))

    def update(self, id, label=None, comment=None):
        # WIP update not working
        # TODO: docu string
        deploy_key = self.get(id)
        data = {}
        # TODO: do data manage if no values for label and comment
        data = {}
        data["key"]=deploy_key.key
        data["comment"] = comment
        data["label"] = label
        logger.warning("WIP     -----")
        logger.debug(f"id:{id} \n data:{data}")

        return self.__get_object(self.put(id, data=data))

    def remove(self, id):
        """
        delete a deploy keys in this repository.
        :param id: string: The deploy key id
        :return:
        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/deploy-keys/%7Bkey_id%7D#delete
        """
        return self.delete(id)

    def get(self, id):
        """
        Returns the deploy keys in this repository.
        :param id: string: The requested deploy key
        :return: The requested DeployKey object, None if not a there are no keys
        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/deploy-keys
        """
        deploy_key = None
        try:
            deploy_key = self.__get_object(super(DeployKeys, self).get(id))
        except HTTPError as e:
            # A 404 indicates that the specified id is not in deploy keys.
            if not e.response.status_code == 404:
                # Rethrow the exception
                raise

        return deploy_key


class DeployKey(BitbucketCloudBase):
    def __init__(self, data, *args, **kwargs):
        super(DeployKey, self).__init__(None, *args, data=data, expected_type="deploy_key", **kwargs)

    @property
    def label(self):
        return str(self.get_data("label"))

    @property
    def key(self):
        return self.get_data("key")

    @property
    def id(self):
        return self.get_data("id")
