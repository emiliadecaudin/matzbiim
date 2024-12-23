from matzbiim import exceptions


def test_skipelement() -> None:
    try:
        raise exceptions.SkipElement()
    except exceptions.SkipElement as err:
        assert isinstance(err, exceptions.SkipElement)
