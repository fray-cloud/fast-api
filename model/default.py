from pydantic import BaseModel, Field, model_validator
from typing import Any, Union
from enum import Enum

class DefaultIn(BaseModel):
    '''
    @var service_key : 공공데이터포털에서 발급받은 인증키
    @var _type : xml(기본값) 또는 json
    '''
    type : str = Field(default='json', alias='_type')

class DefaultOut(BaseModel):
    '''
    
    '''
    class Response(BaseModel):
        class Header(BaseModel):
            reqNo : Union[str, int]
            resultCode : str
            resultMsg : str
            errorMsg : str | None = None
        header : Header
        body : Any
    response : Response