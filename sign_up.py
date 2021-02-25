import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

# event function
def lambda_handler(event, context):
    
    # DynamoDB 불러오기
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('cafe_point')
    
    
    # 카카오 챗봇으로부터 사용자가 입력한 핸드폰 번호 받아오기
    request_body = json.loads(event['body'])
    phone = str(request_body['action']['params']['phone'])
    first_point = 100
    
    # DB에서 핸드폰 번호 조회
    response = table.query(
        
        KeyConditionExpression = Key('phone').eq(phone)
        
    )
    
    items = response['Items']
    
    # DB에 핸드폰 번호 등록
    if not items:
        table.put_item(
            Item={
                'phone' : phone,
                'point' : str(first_point)+"          ",
            }
        )
    
        # 가입 환영 
        result = {
            "version" : "2.0",
            "template":{
                "outputs":[
                    {
                        "simpleText":{
                            "text": "회원가입을 진심으로 환영합니다.\n첫 가입 기념 100포인트을 지급받으셨습니다. ^.^"
                        }
                    }
                    ]
            }
        }

    # 이미 등록된 회원일 경우
    else:
        result = {
            "version" : "2.0",
            "template":{
                "outputs":[
                    {
                        "simpleText":{
                            "text": "이미 회원으로 등록되어 있습니다."
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
