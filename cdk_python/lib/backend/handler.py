"""
Lambda ルーティングハンドラー

API Gatewayからのリクエストを受け取り、
エンドポイントとHTTPメソッドに応じて適切なハンドラーに処理を委譲します。

構造:
    backend/
        handler.py                  (このファイル: ルーティング処理)
        app/
            hello/
                get/
                    app.py          (GET /hello の処理)
            items/
                get/
                    app.py          (GET /items の処理)
                post/
                    app.py          (POST /items の処理) ※将来実装
                put/
                    app.py          (PUT /items の処理) ※将来実装
                delete/
                    app.py          (DELETE /items の処理) ※将来実装
"""
import json
import sys
import os

# app モジュールをインポートパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from hello.get import app as hello_get
from items.get import app as items_get


def handler(event, context):
    """
    メインのLambdaハンドラー
    
    リクエストをパースし、適切なハンドラーにルーティングします。
    
    Args:
        event: API Gatewayからのイベント情報
        context: Lambda実行コンテキスト
        
    Returns:
        dict: HTTPレスポンス
    """
    print(f"Received event: {json.dumps(event)}")

    # リクエスト情報の取得
    http_method = event.get('httpMethod', 'UNKNOWN')
    path = event.get('path', '/')
    query_params = event.get('queryStringParameters') or {}
    
    # リクエストボディの取得
    body = {}
    if event.get('body'):
        try:
            body = json.loads(event.get('body', '{}'))
        except json.JSONDecodeError:
            return create_response(400, {'error': 'Invalid JSON in request body'})

    # ルーティングマップ
    # {(path, method): handler_function}
    routes = {
        ('/hello', 'GET'): lambda: hello_get.handler(event, context),
        ('/items', 'GET'): lambda: items_get.handler(event, context, query_params),
        # 将来追加予定:
        # ('/items', 'POST'): lambda: items_post_app.handler(event, context, body),
        # ('/items', 'PUT'): lambda: items_put_app.handler(event, context, body),
        # ('/items', 'DELETE'): lambda: items_delete_app.handler(event, context, query_params),
    }

    # ルーティング処理
    route_key = (path, http_method)
    
    if route_key in routes:
        try:
            # 対応するハンドラーを実行
            result = routes[route_key]()
            # ハンドラーからのレスポンスをHTTPレスポンスに変換
            return create_response(result['statusCode'], result['body'])
        except Exception as e:
            print(f"Error in handler: {str(e)}")
            return create_response(500, {
                'error': 'Internal Server Error',
                'message': str(e)
            })
    else:
        # 定義されていないエンドポイント/メソッドの組み合わせ
        if any(path == p for p, m in routes.keys()):
            # パスは存在するがメソッドが未対応
            return create_response(405, {
                'error': 'Method Not Allowed',
                'path': path,
                'method': http_method
            })
        else:
            # パス自体が存在しない
            return create_response(404, {
                'error': 'Not Found',
                'path': path
            })


def create_response(status_code, body_dict):
    """
    CORS対応のHTTPレスポンスを生成
    
    Args:
        status_code: HTTPステータスコード
        body_dict: レスポンスボディ (dict)
        
    Returns:
        dict: API Gateway形式のHTTPレスポンス
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
        },
        'body': json.dumps(body_dict, ensure_ascii=False)
    }
