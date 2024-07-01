from .default import BaseModel

class PageIn(BaseModel):
    '''
    @var num_of_rows : 한 페이지 결과 수 (1,000 이하)
    @var page_no : 페이지 번호
    '''
    numOfRows : int
    pageNo : int | None = None

class PageOut(PageIn):
    '''
    @var num_of_rows : 한 페이지 결과 수 (1,000 이하)
    @var page_no : 페이지 번호
    @var total_count : 전체 결과 수
    '''
    totalCount : int

