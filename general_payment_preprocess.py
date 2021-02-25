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
    menu = str(request_body['action']['params']['menu'])
    phone = str(request_body['action']['params']['phone'])
    num = int(request_body['action']['params']['num'])
    
    # payment.py 코드의 API 주소
    webLink = "https://****************.amazonaws.com/default/payment/?"
    
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
    
    # 결제 후 적립할 포인트 계산
    point = int(total_amount * 0.1)
    

    # API 주소 뒤에 Query 형식으로 결제 시 필요한 데이터 첨부
    dic_query = {
        'item_name': menu,
        'quantity': num,
        'total_amount' : total_amount
        }

    dic_encoding = parse.urlencode(dic_query, encoding='UTF-8', doseq=True)

    webLinkUrl = webLink + dic_encoding
    
    # DB로부터 포인트 조회 후 기존 값에 적립할 포인트 값을 더해줌
    response = table.query(
        
        KeyConditionExpression = Key('phone').eq(phone)
        
    )
    
    items = response['Items']
    
    #  비회원일 때, 카카오 챗봇 발화 설정
    if not items :
       
        # 결제 정보를 알려주는 발화 설정
        result = {
            "version":"2.0",
            "template":{
                "outputs":[
                    {
                        "commerceCard":{
                            "description":menu +" "+str(num)+"잔\n비회원은 포인트 적립 X",
                            "price":total_amount,
                            "currency":"won",
                            "thumbnails":[{
                                "imageUrl":"******************",           # 이미지 url
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
        
    # 회원일 때, 기존에 저장되어있는 포인트 값에 적립할 포인트를 더해준다.
    else :
        items =str(items)
        db_point = int(items[12:20])
        new_point = int(db_point + point)
        
        table.put_item(
            Item={
                'phone' : phone,
                'point' : str(new_point)+"          ",
            }
        )
      
            
    
        # 결제 정보를 알려주는 발화 설정
        result = {
            "version":"2.0",
            "template":{
                "outputs":[
                    {
                        "commerceCard":{
                            "description":menu +" "+str(num)+"잔\n적립 포인트 : "+ str(point),
                            "price":total_amount,
                            "currency":"won",
                            "thumbnails":[{
                                "imageUrl":"**************",    # 이미지 URL 추가
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
        

    return {
        'statusCode': 200,
        'body': json.dumps(result),
        'headers': {
            'Access-Control-Allow-Origin': '*'
        }
    }
