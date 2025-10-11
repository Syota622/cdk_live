from aws_cdk import (
    aws_lambda as _lambda,
)
from constructs import Construct
import os


class ApiLambdaConstruct(Construct):
    """
    Lambda関数を構築するコンストラクト
    
    API Gatewayのバックエンドとして動作するLambda関数を作成します。
    """

    def __init__(
        self, 
        scope: Construct, 
        construct_id: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda関数の作成
        self.function = _lambda.Function(
            self, "ApiHandler",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.handler",
            code=_lambda.Code.from_asset(
                os.path.join(os.path.dirname(__file__), "..", "..", "backend")
            ),
            description="API Gatewayのバックエンド処理を行うLambda関数",
        )

