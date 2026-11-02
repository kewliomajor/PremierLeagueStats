import json
from json import JSONEncoder
from bson import ObjectId
import copy

class StatsEncoder(JSONEncoder):
    def default(self, o):
        # Handle the custom class instance
        if hasattr(o, "__dict__"):
            # We copy the dict so we don't accidentally mutate the original object
            data = o.__dict__.copy()
            if "_id" in data and isinstance(data["_id"], ObjectId):
                data["_id"] = str(data["_id"])
            return data
        # Handle standalone ObjectIds
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)


def to_dict(obj):
    return json.loads(json.dumps(obj, cls=StatsEncoder))


def to_dict_native(obj):
    """Recursively converts objects to dictionaries without converting ObjectIds to strings."""
    if hasattr(obj, "__dict__"):
        obj = obj.__dict__

    if isinstance(obj, dict):
        return {k: to_dict_native(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_dict_native(v) for v in obj]
    else:
        # Returns ObjectIds, strings, ints, etc. exactly as they are
        return copy.copy(obj)