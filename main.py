from fastapi import FastAPI, Depends
import requests, json
from enum import Enum
from fastapi.middleware.cors import CORSMiddleware
import schema
import xmltodict
import datetime as dt

from database.crud.sido import set, get

import os
import time



app = FastAPI()

endpoint = 'http://apis.data.go.kr/1543061/abandonmentPublicSrvc'
encoding = 'GsGMbaDETPd05r326o0ICejVO%2BU%2FXwTQES1Tf8Vl3wL0fuYEMxV%2F3Ai2pLmcPFT9yWXTlE9DwTf7H1dR3ezWgg%3D%3D'

origins = [
    'http://localhost:3000',
    'http://localhost:3001',
    'http://172.30.1.80:3000',
    "https://mini-project-l2dyt7ryh-fray-clouds-projects.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SIDO_DATA = None
SIGUNGU_DATA = list()
KIND_DATA = list()

@app.on_event("startup")
def start():
    global SIDO_DATA
    global SIGUNGU_DATA
    global KIND_DATA
    TRAFFIC_TIME = 0.2
    START_TIME = dt.datetime.now()
    item = schema.SidoIn(numOfRows=17)
    # get sido
    res = requests.get(
        f'{endpoint}/sido?serviceKey={encoding}',
        params=item.model_dump(by_alias=True)
        )
    time.sleep(TRAFFIC_TIME)
    print("get get sido")
    error_code = {}
    for key in schema.SidoOut.Response.Items.item.model_fields.keys():
        error_code.update({key : 'error'})
    res_json = change_json(res, error_code)
    
    SIDO_DATA = schema.SidoOut(**res_json)
    # is ok
    print(f"SIDO_DATA :: {SIDO_DATA}")

    # get sigungu & sido count
    COUNT = 0
    for sido in SIDO_DATA.response.body.items['item']:
        item = schema.SigunguIn(upr_cd=sido.orgCd)
        res = requests.get(
        f'{endpoint}/sigungu?serviceKey={encoding}', 
        params=item.model_dump(by_alias=True)
        )
        time.sleep(TRAFFIC_TIME)
        error_code = {}
        for key in schema.SigunguOut.Response.Items.item.model_fields.keys():
            error_code.update({key : 'error'})
        res_json = change_json(res, error_code)
        SIGUNGU_DATA.append({"upr_cd" : sido.orgCd, "item" : res_json})

        item = schema.AbandonmentIn(upr_cd=sido.orgCd)
        res_json = get_abandonment_public(item)
        time.sleep(TRAFFIC_TIME)
        res_json = schema.AbandonmentOut(**res_json)
        sido.totalCount = res_json.response.body.totalCount
        COUNT = COUNT + 1
    # is ok
    print(f"SIGUNGU_DATA :: {SIGUNGU_DATA}")
    
    # get kind
    COUNT = 0
    for up_kind in schema.kind.UpKind:
        item = schema.KindIn(up_kind_cd=up_kind)
        res = requests.get(
        f'{endpoint}/kind?serviceKey={encoding}', 
        params=item.model_dump(by_alias=True)
        )
        time.sleep(TRAFFIC_TIME)
        print(f"get get sigungu {COUNT} times")
        error_code = {}
        no_data_code = {}
        for key in schema.KindOut.Response.Items.item.model_fields.keys():
            error_code.update({key : 'error'})
            if key == "knm" :
                no_data_code.update({key : '전체'})
            else :
                no_data_code.update({key : '-1'})
        
        code = error_code if item.up_kind_cd != '-1' else no_data_code
        print(item.up_kind_cd, code)
        res_json = change_json(res,code)
        KIND_DATA.append({"up_kind_cd" : up_kind.value, "item" : res_json})
        COUNT = COUNT + 1
    # is ok
    print(f"KIND_DATA :: {KIND_DATA}")
    print(f"success spend time :: {dt.datetime.now() - START_TIME}")
    
@app.get("/")
async def get_root():
    print(f"SIDO_DATA :: {SIDO_DATA}")
    print(f"SIGUNGU_DATA :: {SIGUNGU_DATA}")
    print(f"KIND_DATA :: {KIND_DATA}")
    return {'hello' : 'world'}

def change_json(data : requests.Response, error_code : dict):
    res = {}
    # print(f'raw data : \n{data.text}')
    # print(f'data request url : {data.url}')
    print(f'data request status : {data.status_code}')
    # print(f'error_code : {error_code}')
    try :
        if data.text in 'OpenAPI_ServiceResponse':
            raise requests.exceptions.JSONDecodeError
        data_json = data.json()
        
    except requests.exceptions.JSONDecodeError as e:
        data_xml = xmltodict.parse(data.text)
        res['response'] = {}
        res['response']['header'] = {
            "reqNo": "error",
            "resultCode": data_xml['OpenAPI_ServiceResponse']['cmmMsgHeader']['returnReasonCode'],
            "resultMsg": data_xml['OpenAPI_ServiceResponse']['cmmMsgHeader']['errMsg'],
            "errorMsg": data_xml['OpenAPI_ServiceResponse']['cmmMsgHeader']['returnAuthMsg'],
        }
        res['response']['body'] = {
            'numOfRows' : 0,
            'pageNo' : 0,
            'totalCount' : 0,
            'reqNo' : 'error'
        }
        res['response']['body']['items'] = {}
        res['response']['body']['items']['item'] = [error_code]
        print(json.dumps(res))
        return res
    else:
        if data_json['response']['header']['resultCode'] != '00':
            data_json['response']['body'] = {
                'items' : {
                            'item' : [
                                error_code,
                            ]
                        }
            }
        return data_json


@app.get("/sido/db", response_model=schema.SidoOut)
async def get_sido_by_db():
    # step 1
    data = await get()
    print([schema.SidoOut.Response.Items.item(orgCd=item.orgCd, orgdownNm=item.orgdownNm) for item in data])
    result = schema.SidoOut(
        response=schema.SidoOut.Response(
            header=schema.SidoOut.Response.Header(
                reqNo=f"{dt.date.today()}",
                resultCode="DB",
                resultMsg="NOMAL",
            ),
            body=schema.SidoOut.Response.Items(
                numOfRows=data.__len__(),
                totalCount=data.__len__(),
                items={"item" : [schema.SidoOut.Response.Items.item(orgCd=item.orgCd, orgdownNm=item.orgdownNm).model_dump() for item in data]}
            )
        )
    )
    return result

@app.get("/sido", response_model=schema.SidoOut)
def get_sido():
    return SIDO_DATA

@app.get("/sido/count", response_model=schema.SidoOut)
async def get_sido_count():
    document_find = schema.SidoOut.find(
        schema.SidoOut.site_updated == dt.date.today()
    )
    print(await document_find.to_list())
    pass



@app.get("/sigungu", response_model=schema.SigunguOut)
async def get_sigungu(item : schema.SigunguIn = Depends()):
    res_json = None
    for sigungu in SIGUNGU_DATA:
        if sigungu["upr_cd"] == item.upr_cd:
            res_json = sigungu["item"]
    return res_json


@app.get("/kind", response_model=schema.KindOut)
def get_kind(item : schema.KindIn = Depends()):
    res_json = None
    for kind in KIND_DATA:
        if kind["up_kind_cd"] == item.up_kind_cd:
            res_json = kind["item"]
    return res_json
 
@app.get("/abandonmentPublic", response_model=schema.AbandonmentOut)
def get_abandonment_public(item : schema.AbandonmentIn = Depends()):
    edit_item = item.model_dump(by_alias=True)
    
    for key in edit_item:
        if edit_item[key] == '-1':
            edit_item.update({key : None})

    res = requests.get(
        f'{endpoint}/abandonmentPublic?serviceKey={encoding}', 
        # params=item.model_dump(by_alias=True)
        params=edit_item,
        )
    
    error_code = {}
    # no_data_code = {}
    for key in schema.AbandonmentOut.Response.Items.item.model_fields.keys():
        error_code.update({key : 'error'})

    res_json = change_json(res,error_code)
    return res_json

