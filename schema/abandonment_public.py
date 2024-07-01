from .default import Union, BaseModel, model_validator, DefaultIn, DefaultOut
from .page import PageIn, PageOut

class AbandonmentIn(DefaultIn, PageIn):
    bgnde: Union[str, None] = None # 유기날짜 시작일
    endde: Union[str, None] = None # 유기날짜 종료일
    upkind: Union[str, None] = None  # 축종코드
    kind: Union[str, None] = None  # 품종코드
    upr_cd: Union[str, None] = None  # 시도코드
    org_cd: Union[str, None] = None  # 시군구코드
    care_reg_no: Union[str, None] = None  # 보호소번호
    state: Union[str, None] = None  # 상태
    neuter_yn: Union[str, None] = None  # 중성화여부
    pageNo: Union[str, None] = None  # 페이지 번호
    numOfRows: int = 10  # 페이지당 보여줄 갯수

    @model_validator(mode='after')
    def set_model(self):
        if self.org_cd == '-1':
            self.org_cd = None
        if self.kind == '-1':
            self.kind = None
        return self

class AbandonmentOut(BaseModel):
    class Response(DefaultOut.Response):
        class Items(PageOut):
            class item(BaseModel):
                desertionNo : str # 유기번호
                filename : str # 썸네일 이미지(링크)
                happenDt : str # 접수일 YYYYMMDD
                happenPlace : str # 발견장소
                kindCd : str # 품종
                colorCd : str # 색상
                age : str # 나이
                weight : str # 체중
                noticeNo : str # 공고번호
                noticeSdt : str # 공고 시작일 YYYYMMDD
                noticeEdt : str # 공고 종료일 YYYYMMDD
                popfile : str # 이미지(링크)
                processState : str # 상태
                sexCd : str # 성별 M : 남 F : 여 Q : 미상
                neuterYn : str # 중성화 여부 Y : 예 N : 아니오 U : 미상
                specialMark : str # 특징
                careNm : str # 보호소 이름
                careTel : str # 보호소 전화번호
                careAddr : str # 보호장소
                orgNm : str # 관할기관
                chargeNm : Union[str, None] = None # 담당자
                officetel : str #  담당자 연락처
                noticeComment : Union[str, None] = None # 특이사항

            items : dict[str, list[item]]
        body : Items
    response : Response

    class Settings:
        name ='abandonment'