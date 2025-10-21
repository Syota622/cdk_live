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
        pj_name: str,
        env_name: str,
        lambda_function: _lambda.Function,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # API Gatewayの作成
        self.api = apigw.LambdaRestApi(
            self, "SimpleApi",
            handler=lambda_function,
            proxy=False,
            rest_api_name=f"{pj_name}-{env_name}-rest-api",
            description="CDK Pythonで作成したシンプルなREST API",
            deploy_options=apigw.StageOptions(
                stage_name=env_name,  # ステージ名を環境名に設定（dev/stg/prod）
            ),
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
        /items エンドポイントを追加
        
        IDの取得や処理はLambda関数側で実装します。
        - GET /items?id=xxx : 特定アイテム取得
        - GET /items : アイテム一覧取得
        - POST /items : アイテム作成
        - PUT /items : アイテム更新（IDはリクエストボディに含む）
        - DELETE /items?id=xxx : アイテム削除
        """
        # /items エンドポイント
        items = self.api.root.add_resource("items")
        items.add_method("GET")     # アイテム一覧取得 or 特定アイテム取得（クエリパラメータでid指定）
        items.add_method("POST")    # アイテム作成
        items.add_method("PUT")     # アイテム更新（リクエストボディにid含む）
        items.add_method("DELETE")  # アイテム削除（クエリパラメータでid指定）
        


