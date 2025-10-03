class UnauthenticatedException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DuplicateModelException(Exception):
    def __init__(self, attribute_name: str, *args: object) -> None:
        super().__init__(*args)
        self.attribute_name = attribute_name


class ModelNotFoundException(Exception):
    def __init__(self, model_name: str, model_id: int, *args: object) -> None:
        super().__init__(*args)
        self.model_name = model_name
        self.model_id = model_id


class PermissionException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)