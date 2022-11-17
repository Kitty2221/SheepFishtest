import json
from django.db.models.fields.json import JSONField


class ReadableJSONFormField(JSONField):
    def prepare_value(self, value):
        print(value)
        return json.dumps(value, ensure_ascii=False, indent=4)
