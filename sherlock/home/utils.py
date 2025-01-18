import logging

logger = logging.getLogger(__file__)


def get_object_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.MultipleObjectsReturned as _:
        logger.error(f"Multiple objects returned of model {classmodel}")
    except classmodel.DoesNotExist:
        return None


def asdict_with_properties(obj):
    """
    Similar to dataclasses.asdict, but passes also dataclass properties that are functions.
    """
    return {
        prop: getattr(obj, prop)
        for prop in dir(obj)
        if not (prop.startswith("__") or callable(getattr(obj, prop, None)))
    }
