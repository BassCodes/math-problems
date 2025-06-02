class DraftPublishError(Exception):
    def __init__(self, message):
        super().__init__(message)


class DraftDependsOnOtherDraft(DraftPublishError):
    def __init__(self, message):
        super().__init__(message)


class DraftCreationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class AttemptToDoubleForkObject(Exception):
    def __init__(self, message):
        super().__init__(message)
