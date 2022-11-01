from pydantic import BaseModel, Extra


class DataModel(BaseModel, extra=Extra.forbid):
    pass
