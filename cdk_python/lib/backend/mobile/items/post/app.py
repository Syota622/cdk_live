"""
POST /items エンドポイントの処理

新しいアイテムをDynamoDBに追加します。
"""
import os
import boto3
import uuid
from datetime import datetime


# DynamoDBクライアントの初期化
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('ITEMS_TABLE_NAME')
table = dynamodb.Table(table_name)


def handler(event, context, body):
    """
    POST /items のハンドラー
    
    Args:
        event: API Gatewayからのイベント情報
        context: Lambda実行コンテキスト
        body: リクエストボディ（dict）
        
    Returns:
        dict: HTTPレスポンス
    """
    try:
        # リクエストボディのバリデーション
        if not body:
            return {
                'statusCode': 400,
                'body': {
                    'error': 'Bad Request',
                    'message': 'Request body is required',
                    'endpoint': '/items',
                    'method': 'POST'
                }
            }
        
        # 必須フィールドのチェック
        name = body.get('name')
        if not name:
            return {
                'statusCode': 400,
                'body': {
                    'error': 'Bad Request',
                    'message': 'Field "name" is required',
                    'endpoint': '/items',
                    'method': 'POST'
                }
            }
        
        # アイテムの作成
        item_id = str(uuid.uuid4())  # UUIDを生成
        timestamp = datetime.utcnow().isoformat()
        
        # priceを数値型に変換（Decimal型を避けるため）
        price = body.get('price', 0)
        if isinstance(price, (int, float)):
            price = int(price) if isinstance(price, int) else float(price)
        else:
            price = 0
        
        item = {
            'id': item_id,
            'name': name,
            'description': body.get('description', ''),
            'price': price,
            'created_at': timestamp,
            'updated_at': timestamp
        }
        
        # DynamoDBに保存
        table.put_item(Item=item)
        
        return {
            'statusCode': 201,
            'body': {
                'message': 'Item created successfully',
                'item': item,
                'endpoint': '/items',
                'method': 'POST',
                'request_id': context.aws_request_id
            }
        }
    
    except Exception as e:
        # エラーハンドリング
        print(f"Error creating item in DynamoDB: {str(e)}")
        return {
            'statusCode': 500,
            'body': {
                'error': 'Internal server error',
                'message': str(e),
                'endpoint': '/items',
                'method': 'POST',
                'request_id': context.aws_request_id
            }
        }

