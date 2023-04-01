from pydantic import BaseModel

class RequestTarget(BaseModel):
    id: int
    type: str
    regions: None
    letter : Union[str,None] = None
    letter_color : Union[str,None] = None
    shape :  Union[str,None] = None
    shape_color :  Union[str,None] = None
    orientation:  Union[int,None] = None
    notes :  Union[str,None] = None