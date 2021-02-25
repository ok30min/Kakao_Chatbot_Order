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
    

    # 포인트 조회
    response = table.query(
        
        KeyConditionExpression=Key('phone').eq(phone)
        
    )
    
    items = response['Items']
    
    # 비회원일 경우
    if not items:
        result = {
            "version" : "2.0",
            "template":{
                "outputs":[
                    {
                        "simpleText":{
                            "text": "고객님은 회원으로 등록되어 있지않습니다."
                        }
                    }
                    ]
            }
        }
        
    # 회원일 경우
    else:
        items = str(items)
        point = int(items[12:19])
        result = {
            "version" : "2.0",
            "template":{
                "outputs":[
                    {
                        "simpleText":{
                            "text": "고객님은 현재 \n"+str(point)+"포인트를 보유중이십니다."
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
