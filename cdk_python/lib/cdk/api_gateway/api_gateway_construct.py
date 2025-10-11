from aws_cdk import (
    aws_apigateway as apigw,
    aws_lambda as _lambda,
)
from constructs import Construct


class ApiGatewayConstruct(Construct):
    """
    API Gatewayを構築するコンストラクト
    
    Lambda関数を統合したREST APIを作成し、各エンドポイントを設定します。
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        lambda_function: _lambda.Function,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # API Gatewayの作成
        self.api = apigw.LambdaRestApi(
            self, "SimpleApi",
            handler=lambda_function,
            proxy=False,
            rest_api_name="Simple REST API",
            description="CDK Pythonで作成したシンプルなREST API",
        )

        # /hello エンドポイントの追加
        self._add_hello_endpoint()
        
        # /items エンドポイントの追加
        self._add_items_endpoints()

    def _add_hello_endpoint(self) -> None:
        """
        /hello エンドポイントを追加
        """
        hello = self.api.root.add_resource("hello")
        hello.add_method("GET")

    def _add_items_endpoints(self) -> None:
        """
        /items と /items/{id} エンドポイントを追加
        """
        # /items エンドポイント
        items = self.api.root.add_resource("items")
        items.add_method("GET")   # アイテム一覧取得
        items.add_method("POST")  # アイテム作成

        # /items/{id} エンドポイント
        item = items.add_resource("{id}")
        item.add_method("GET")     # 特定アイテム取得
        item.add_method("PUT")     # アイテム更新
        item.add_method("DELETE")  # アイテム削除

