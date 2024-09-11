from typing import Literal


class Response:
    retrieval: bool = False
    action: Literal['find', 'countDocuments', 'aggregate']
    query: dict = None
    limit: int
    result: list = []
    masked: list
    error_msg: str = None
    llm_response: str = 'Something went wrong. Please try again.'
    valid: bool = False

    def __repr__(self) -> dict:
        return str(self.__dict__)
