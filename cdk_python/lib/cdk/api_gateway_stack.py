from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)
from constructs import Construct
import os


class ApiGatewayStack(Stack):
    """
    API Gateway + Lambda のCDKスタック

    このスタックは以下のリソースを作成します:
    - Lambda関数: API Gatewayからのリクエストを処理
    - API Gateway REST API: RESTful APIエンドポイントを提供
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda関数の作成
        api_lambda = _lambda.Function(
            self, "ApiHandler",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.handler",
            code=_lambda.Code.from_asset(
                os.path.join(os.path.dirname(__file__), "..", "lambda")
            ),
            description="API Gatewayのバックエンド処理を行うLambda関数",
        )

        # API Gatewayの作成
        api = apigw.LambdaRestApi(
            self, "SimpleApi",
            handler=api_lambda,
            proxy=False,
            rest_api_name="Simple REST API",
            description="CDK Pythonで作成したシンプルなREST API",
        )

        # /hello エンドポイントの追加
        hello = api.root.add_resource("hello")
        hello.add_method("GET")

        # /items エンドポイントの追加
        items = api.root.add_resource("items")
        items.add_method("GET")   # アイテム一覧取得
        items.add_method("POST")  # アイテム作成

        # /items/{id} エンドポイントの追加
        item = items.add_resource("{id}")
        item.add_method("GET")     # 特定アイテム取得
        item.add_method("PUT")     # アイテム更新
        item.add_method("DELETE")  # アイテム削除
