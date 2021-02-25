import json
import boto3
from urllib import parse
from boto3.dynamodb.conditions import Key, Attr


# 메뉴
menu_list = ["에스프레소", "핫아메리카노", "핫카푸치노", "핫카페라떼", "핫바닐라라떼", "핫카페모카",
             "핫카라멜마끼아또", "핫아메리카노 더블", "아이스오늘의커피", "아이스아메리카노", "아이스카푸치노",
             "아이스카페라떼", "아이스바닐라라떼", "아이스카페모카", "아이스카라멜마끼아또", "아이스화이트모카",
             "아이스아메리카노 더블"]
             
money_list = [1500, 2000, 2300, 2500, 2800, 2800, 2800, 4000, 3000, 2200, 2500, 2500, 2800, 2800, 2800, 3200, 4400]

# event function
def lambda_handler(event, context):
    
    # DynamoDB 불러오기
    dynamodb = boto3.resource('dynamodb')   
    table = dynamodb.Table('cafe_point')
    
    # 카카오 챗봇으로부터 사용자가 입력한 파라미터 받아오기
    request_body = json.loads(event['body'])
    menu = str(request_body['action']['params']['menu'])      # 사용자가 선택한 메뉴
    phone = str(request_body['action']['params']['phone'])    # 사용자의 핸드폰 번호
    num = int(request_body['action']['params']['num'])         # 사용자가 선택한 메뉴의 수량
    point = int(request_body['action']['params']['paypoint'])  # 결제 시 사용할 포인트의 양
    
    # payment.py 코드의 API 주소
    webLink = "https://************.amazonaws.com/default/payment/?"

    global menu_list
    global money_list

    x = 0

    # 사용자가 선택한 메뉴와 수량에 따른 총 결제 금액 계산
    for x in range(len(menu_list)):
        if menu == menu_list[x]:
            total_amount = int(money_list[x] * num)
            break
        else:
            x = x + 1
    
    # 총 결제 금액에서 사용할 포인트 차감
    total_amount2 = int(total_amount - point)
    

    # API 주소 뒤에 Query 형식으로 결제 시 필요한 데이터 첨부
    dic_query = {
        'item_name': menu,
        'quantity': num,
        'total_amount' : total_amount2
        }

    dic_encoding = parse.urlencode(dic_query, encoding='UTF-8', doseq=True)

    webLinkUrl = webLink + dic_encoding
    
    # DB로부터 포인트 조회 및 차감
    response = table.query(
        
        KeyConditionExpression=Key('phone').eq(phone)
        
    )
    
    items = response['Items']
    
    # 비회원일 때, 카카오 챗봇 발화 설정
    if not items :
        result = {
            "version" : "2.0",
            "template":{
                "outputs":[
                    {
                        "simpleText":{
                            "text": "회원으로 등록되어 있지 않습니다.\n일반 결제로 다시 시도해주세요"
                        }
                    }
                    ]
            }
        }
        
    # 결제 전 카카오 챗봇 발화 설정
    else:
        items =str(items)
        db_point = int(items[12:20])
        new_point = int(db_point - point)
    
        # RESULT
        if new_point >= 0 :
            result = {
                "version":"2.0",
                "template":{
                    "outputs":[
                        {
                            "commerceCard":{
                                "description": menu +" "+str(num)+"잔\n사용 포인트 : "+ str(point),
                                "price":total_amount,
                                "discount": point,
                                "currency":"won",
                                "thumbnails":[{
                                    "imageUrl":"https://**************",           # 이미지 URL 설정
                                    "link":{
                                        "web": webLinkUrl
                                    }
                                }],
                                "buttons":[
                                    {
                                        "label":"결제하기",
                                        "action":"webLink",
                                        "webLink":webLinkUrl
                                    }
                                    ]
                            }
                        }]
                }
            }
            
            table.put_item(
                Item={
                    'phone' : phone,
                    'point' : str(new_point)+"          ",
                }
            )
        else:
            result = {
                "version" : "2.0",
                "template":{
                    "outputs":[
                        {
                            "simpleText":{
                                "text": "보유한 포인트보다 많은 포인트금액은 사용하지 못합니다."
                            }
                        }
                        ]
                }
            }
    
    return {
        'statusCode': 200,
        'body': json.dumps(result),
        'headers': {
            'Access-Control-Allow-Origin': '*'
        }
    }
