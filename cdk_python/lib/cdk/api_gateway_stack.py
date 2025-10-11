from aws_cdk import Stack
from constructs import Construct

from .lambda_function.lambda_construct import ApiLambdaConstruct
from .api_gateway.api_gateway_construct import ApiGatewayConstruct


class ApiGatewayStack(Stack):
    """
    API Gateway + Lambda のCDKスタック

    このスタックは以下のリソースを作成します:
    - Lambda関数: API Gatewayからのリクエストを処理
    - API Gateway REST API: RESTful APIエンドポイントを提供
    
    リファクタリングにより、Lambda と API Gateway は
    それぞれ独立したコンストラクトとして管理されています。
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda関数の作成
        lambda_construct = ApiLambdaConstruct(self, "LambdaConstruct")

        # API Gatewayの作成
        api_gateway_construct = ApiGatewayConstruct(
            self, "ApiGatewayConstruct",
            lambda_function=lambda_construct.function
        )

        # 作成されたリソースへの参照を保持
        self.lambda_function = lambda_construct.function
        self.api = api_gateway_construct.api
