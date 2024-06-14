from fastapi import FastAPI, Depends
import requests, json
from enum import Enum
from fastapi.middleware.cors import CORSMiddleware
import model
import xmltodict


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

@app.get("/sido", response_model=model.SidoOut)
async def get_sido(item : model.SidoIn = Depends()):
    res = requests.get(
        f'{endpoint}/sido?serviceKey={encoding}',
        params=item.model_dump(by_alias=True)
        )

    error_code = {}
    for key in model.SidoOut.Response.Items.item.model_fields.keys():
        error_code.update({key : 'error'})
    res_json = change_json(res, error_code)
    # await model.mongodb.engine.save()
    return res_json


@app.get("/sigungu", response_model=model.SigunguOut)
def get_sigungu(item : model.SigunguIn = Depends()):
    res = requests.get(
        f'{endpoint}/sigungu?serviceKey={encoding}', 
        params=item.model_dump(by_alias=True)
        )
    
    error_code = {}
    no_data_code = {}
    for key in model.SigunguOut.Response.Items.item.model_fields.keys():
        error_code.update({key : 'error'})
        if key == "orgdownNm" :
            no_data_code.update({key : '전체'})
        else :
            no_data_code.update({key : '-1'})
    
    code = error_code if item.upr_cd != '-1' else no_data_code
    print('sigungu item.upr_cd', item.upr_cd, code)
    res_json = change_json(res,code)
    return res_json


@app.get("/kind", response_model=model.KindOut)
def get_kind(item : model.KindIn = Depends()):
    res = requests.get(
        f'{endpoint}/kind?serviceKey={encoding}', 
        params=item.model_dump(by_alias=True)
        )
    
    error_code = {}
    no_data_code = {}
    for key in model.KindOut.Response.Items.item.model_fields.keys():
        error_code.update({key : 'error'})
        if key == "knm" :
            no_data_code.update({key : '전체'})
        else :
            no_data_code.update({key : '-1'})
    
    code = error_code if item.up_kind_cd != '-1' else no_data_code
    print(item.up_kind_cd, code)
    res_json = change_json(res,code)
    return res_json
 
@app.get("/abandonmentPublic", response_model=model.AbandonmentOut)
def get_abandonment_public(item : model.AbandonmentIn = Depends()):
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
    for key in model.AbandonmentOut.Response.Items.item.model_fields.keys():
        error_code.update({key : 'error'})

    res_json = change_json(res,error_code)
    return res_json

