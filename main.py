from fastapi import FastAPI, Depends
import requests, json
from enum import Enum
from fastapi.middleware.cors import CORSMiddleware
import schema
import xmltodict
import datetime as dt

from database.crud.sido import set, get

import os



app = FastAPI()

endpoint = 'http://apis.data.go.kr/1543061/abandonmentPublicSrvc'
encoding = 'GsGMbaDETPd05r326o0ICejVO%2BU%2FXwTQES1Tf8Vl3wL0fuYEMxV%2F3Ai2pLmcPFT9yWXTlE9DwTf7H1dR3ezWgg%3D%3D'

origins = [
    'http://localhost:3000',
    'http://localhost:3001',
    'http://172.30.1.80:3000',
    "https://mini-project-l2dyt7ryh-fray-clouds-projects.vercel.app",
    "https://mini-project-mocha.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.on_event("startup")
# async def start_db():
#     await model.mongodb.connect()


@app.get("/")
async def get_root():
    return {'hello' : 'world'}

def change_json(data : requests.Response, error_code : dict):
    res = {}
    print(f'raw data : \n{data.text}')
    print(f'data request url : {data.url}')
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
        print(json.dumps(res, indent=2))
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

# @app.post("/sido", response_model=model.SidoOut)
# async def post_sido(item : model.SidoIn = Depends()):
#     res = requests.get(
#         f'{endpoint}/sido?serviceKey={encoding}',
#         params=item.model_dump(by_alias=True)
#         )
    

@app.get("/sido/db", response_model=schema.SidoOut)
async def get_sido_by_db():
    # res = requests.get(
    #     f'{endpoint}/sido?serviceKey={encoding}',
    #     params=item.model_dump(by_alias=True)
    #     )

    # error_code = {}
    # for key in schema.SidoOut.Response.Items.item.model_fields.keys():
    #     error_code.update({key : 'error'})
    # res_json = change_json(res, error_code)
    # res_json = schema.SidoOut(**res_json)
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
def get_sido(item : schema.SidoIn = Depends()):
    res = requests.get(
        f'{endpoint}/sido?serviceKey={encoding}',
        params=item.model_dump(by_alias=True)
        )

    error_code = {}
    for key in schema.SidoOut.Response.Items.item.model_fields.keys():
        error_code.update({key : 'error'})
    res_json = change_json(res, error_code)
    return res_json

@app.get("/sido/count", response_model=schema.SidoOut)
async def get_sido_count():
    document_find = schema.SidoOut.find(
        schema.SidoOut.site_updated == dt.date.today()
    )
    print(await document_find.to_list())
    pass



@app.get("/sigungu", response_model=schema.SigunguOut)
async def get_sigungu(item : schema.SigunguIn = Depends()):
    res = requests.get(
        f'{endpoint}/sigungu?serviceKey={encoding}', 
        params=item.model_dump(by_alias=True)
        )
    
    error_code = {}
    no_data_code = {}
    for key in schema.SigunguOut.Response.Items.item.model_fields.keys():
        error_code.update({key : 'error'})
        if key == "orgdownNm" :
            no_data_code.update({key : '전체'})
        else :
            no_data_code.update({key : '-1'})
    
    code = error_code if item.upr_cd != '-1' else no_data_code
    print('sigungu item.upr_cd', item.upr_cd, code)
    res_json = change_json(res,code)
    # print('dma...')
    # print(model.SigunguOut.response.body.items.get("upr_cd"))
    await schema.SigunguOut(sido_id=item.model_dump().get("upr_cd"), **res_json).insert()
    return res_json


@app.get("/kind", response_model=schema.KindOut)
def get_kind(item : schema.KindIn = Depends()):
    res = requests.get(
        f'{endpoint}/kind?serviceKey={encoding}', 
        params=item.model_dump(by_alias=True)
        )
    
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

