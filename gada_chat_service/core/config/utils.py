import dataclasses, json
from json import JSONEncoder


class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)


class EmployeeEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
