"""
GET /items エンドポイントの処理

アイテムの一覧取得または特定アイテムの取得を行います。
クエリパラメータに id が指定されている場合は特定アイテムを、
指定されていない場合は全アイテムを返します。
"""


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
    # クエリパラメータに id が含まれているかチェック
    item_id = query_params.get('id')
    
    if item_id:
        # 特定のアイテムを返す
        return {
            'statusCode': 200,
            'body': {
                'id': item_id,
                'name': f'Item {item_id}',
                'description': f'This is item {item_id}',
                'endpoint': '/items',
                'method': 'GET',
                'request_id': context.aws_request_id
            }
        }
    else:
        # 全アイテムのリストを返す
        return {
            'statusCode': 200,
            'body': {
                'items': [
                    {'id': '1', 'name': 'Item 1'},
                    {'id': '2', 'name': 'Item 2'},
                    {'id': '3', 'name': 'Item 3'}
                ],
                'count': 3,
                'endpoint': '/items',
                'method': 'GET',
                'request_id': context.aws_request_id
            }
        }

