from unittest.mock import AsyncMock


def construct_class(name):
    """
    Using this function you can create mock class
    :param name:
    :return:s
    """
    instance = AsyncMock()
    instance._name_of_parent_class = name
    constructor = AsyncMock(return_value=instance)
    return constructor
