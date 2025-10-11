from aws_cdk import Stack
from constructs import Construct

from .lambda_function.mobile.mobile_hello_get import ApiLambdaConstruct
from .api_gateway.mobile.api_gateway import ApiGatewayConstruct


class ApiGatewayStack(Stack):
    """
    API Gateway + Lambda のCDKスタック

    このスタックは以下のリソースを作成します:
    - Lambda関数: API Gatewayからのリクエストを処理
    - API Gateway REST API: RESTful APIエンドポイントを提供
    
    リファクタリングにより、Lambda と API Gateway は
    それぞれ独立したコンストラクトとして管理されています。
    
    フォルダ構造:
        cdk/
            common_stack.py                 (このファイル)
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
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda関数の作成
        mobile_hello_get = ApiLambdaConstruct(
            self, "LambdaConstruct",
            pj_name=pj_name
        )

        # API Gatewayの作成
        api_gateway_construct = ApiGatewayConstruct(
            self, "ApiGatewayConstruct",
            pj_name=pj_name,
            lambda_function=mobile_hello_get.function
        )

        # 作成されたリソースへの参照を保持
        self.lambda_function = mobile_hello_get.function
        self.api = api_gateway_construct.api
