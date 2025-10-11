"""
GET /hello エンドポイントの処理

シンプルな挨拶メッセージを返します。
"""


def handler(event, context):
    """
    GET /hello のハンドラー
    
    Args:
        event: API Gatewayからのイベント情報
        context: Lambda実行コンテキスト
        
    Returns:
        dict: HTTPレスポンス
    """
    return {
        'statusCode': 200,
        'body': {
            'message': 'Hello from API Gateway!',
            'endpoint': '/hello',
            'method': 'GET',
            'request_id': context.aws_request_id
        }
    }

