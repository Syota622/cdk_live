"""
GET /items エンドポイントの処理

アイテムの一覧取得または特定アイテムの取得を行います。
クエリパラメータに id が指定されている場合は特定アイテムを、
指定されていない場合は全アイテムを返します。
"""
import os
import boto3
from decimal import Decimal


# DynamoDBクライアントの初期化
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('ITEMS_TABLE_NAME')
table = dynamodb.Table(table_name)


def decimal_to_float(obj):
    """DynamoDBの Decimal 型を float に変換"""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def handler(event, context, query_params):
    """
    GET /items のハンドラー
    
    Args:
        event: API Gatewayからのイベント情報
        context: Lambda実行コンテキスト
        query_params: クエリパラメータ
        
    Returns:
        dict: HTTPレスポンス
    """
    try:
        # クエリパラメータに id が含まれているかチェック
        item_id = query_params.get('id')
        
        if item_id:
            # 特定のアイテムを取得
            response = table.get_item(Key={'id': item_id})
            
            if 'Item' in response:
                item = response['Item']
                return {
                    'statusCode': 200,
                    'body': {
                        'item': item,
                        'endpoint': '/items',
                        'method': 'GET',
                        'request_id': context.aws_request_id
                    }
                }
            else:
                # アイテムが見つからない
                return {
                    'statusCode': 404,
                    'body': {
                        'error': 'Item not found',
                        'id': item_id,
                        'endpoint': '/items',
                        'method': 'GET',
                        'request_id': context.aws_request_id
                    }
                }
        else:
            # 全アイテムをスキャン（取得）
            response = table.scan()
            items = response.get('Items', [])
            
            return {
                'statusCode': 200,
                'body': {
                    'items': items,
                    'count': len(items),
                    'endpoint': '/items',
                    'method': 'GET',
                    'request_id': context.aws_request_id
                }
            }
    
    except Exception as e:
        # エラーハンドリング
        print(f"Error accessing DynamoDB: {str(e)}")
        return {
            'statusCode': 500,
            'body': {
                'error': 'Internal server error',
                'message': str(e),
                'endpoint': '/items',
                'method': 'GET',
                'request_id': context.aws_request_id
            }
        }

