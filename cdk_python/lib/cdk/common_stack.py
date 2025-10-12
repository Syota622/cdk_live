from aws_cdk import Stack
from constructs import Construct

from .lambda_function.mobile.mobile_hello_get import ApiLambdaConstruct
from .api_gateway.mobile.api_gateway import ApiGatewayConstruct
from .database.dynamodb import DynamoDBConstruct


class ApiGatewayStack(Stack):
    """
    API Gateway + Lambda + DynamoDB のCDKスタック

    このスタックは以下のリソースを作成します:
    - DynamoDB: データストレージ
    - Lambda関数: API Gatewayからのリクエストを処理
    - API Gateway REST API: RESTful APIエンドポイントを提供
    
    リファクタリングにより、各リソースは独立したコンストラクトとして管理されています。
    
    フォルダ構造:
        cdk/
            common_stack.py                 (このファイル)
            database/
                dynamodb.py                 (DynamoDB構築)
            lambda_function/
                mobile/
                    mobile_hello_get.py     (Lambda構築)
            api_gateway/
                mobile/
                    api_gateway.py          (API Gateway構築)
    """

    def __init__(
        self, 
        scope: Construct, 
        construct_id: str, 
        pj_name: str,
        env_name: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDBテーブルの作成
        dynamodb_construct = DynamoDBConstruct(
            self, "DynamoDBConstruct",
            pj_name=pj_name,
            env_name=env_name
        )

        # Lambda関数の作成
        mobile_hello_get = ApiLambdaConstruct(
            self, "LambdaConstruct",
            pj_name=pj_name,
            env_name=env_name,
            hello_table=dynamodb_construct.hello_table
        )

        # API Gatewayの作成
        api_gateway_construct = ApiGatewayConstruct(
            self, "ApiGatewayConstruct",
            pj_name=pj_name,
            env_name=env_name,
            lambda_function=mobile_hello_get.function
        )

        # 作成されたリソースへの参照を保持
        self.hello_table = dynamodb_construct.hello_table
        self.lambda_function = mobile_hello_get.function
        self.api = api_gateway_construct.api
