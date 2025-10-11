"""
GET /items エンドポイントの処理

アイテム一覧の取得、または特定アイテムの取得を行います。
IDが指定されている場合は特定アイテム、指定されていない場合は一覧を返します。
"""


def handler(event, context, query_params):
    """
    GET /items のハンドラー
    
    Args:
        event: API Gatewayからのイベント情報
        context: Lambda実行コンテキスト
        query_params: クエリパラメータ (dict)
        
    Returns:
        dict: HTTPレスポンス
    """
    item_id = query_params.get('id')
    
    if item_id:
        # 特定アイテムの取得
        return {
            'statusCode': 200,
            'body': {
                'message': f'アイテムID {item_id} の詳細を取得',
                'endpoint': '/items',
                'method': 'GET',
                'item_id': item_id,
                'operation': 'get_item',
                # 実際のDB実装ではここでデータを取得
                'data': {
                    'id': item_id,
                    'name': f'サンプルアイテム {item_id}',
                    'description': 'これはサンプルデータです'
                }
            }
        }
    else:
        # アイテム一覧の取得
        return {
            'statusCode': 200,
            'body': {
                'message': 'アイテム一覧を取得',
                'endpoint': '/items',
                'method': 'GET',
                'operation': 'list_items',
                # 実際のDB実装ではここでデータを取得
                'items': [
                    {'id': '1', 'name': 'サンプルアイテム1'},
                    {'id': '2', 'name': 'サンプルアイテム2'},
                    {'id': '3', 'name': 'サンプルアイテム3'}
                ],
                'count': 3
            }
        }

