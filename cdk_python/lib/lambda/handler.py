import json

def handler(event, context):
    """
    Simple Lambda handler for API Gateway
    """
    print(f"Received event: {json.dumps(event)}")

    # HTTPメソッドを取得
    http_method = event.get('httpMethod', 'UNKNOWN')
    path = event.get('path', '/')

    # レスポンスボディ
    response_body = {
        'message': 'Hello from API Gateway!',
        'method': http_method,
        'path': path,
        'request_id': context.aws_request_id
    }

    # CORS対応のレスポンス
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
        },
        'body': json.dumps(response_body)
    }
