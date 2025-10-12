from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
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
        pj_name: str,
        env_name: str,
        hello_table: dynamodb.Table,
        items_table: dynamodb.Table,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda関数の作成
        self.function = _lambda.Function(
            self, "ApiHandler",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.handler",
            code=_lambda.Code.from_asset(
                os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "backend")
            ),
            function_name=f"{pj_name}-{env_name}-lambda-api-handler",
            description="API Gatewayのバックエンド処理を行うLambda関数",
            environment={
                "HELLO_TABLE_NAME": hello_table.table_name,
                "ITEMS_TABLE_NAME": items_table.table_name,
            }
        )

        # DynamoDBテーブルへのアクセス権限を付与
        hello_table.grant_read_write_data(self.function)
        items_table.grant_read_write_data(self.function)

