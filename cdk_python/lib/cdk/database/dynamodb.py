from aws_cdk import (
    aws_dynamodb as dynamodb,
    RemovalPolicy,
)
from constructs import Construct


class DynamoDBConstruct(Construct):
    """
    DynamoDBテーブルを構築するコンストラクト
    
    各環境用のDynamoDBテーブルを作成します。
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

        # helloテーブルの作成
        self.hello_table = dynamodb.Table(
            self, "HelloTable",
            table_name=f"{pj_name}-{env_name}-hello",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,  # オンデマンド課金
            removal_policy=RemovalPolicy.DESTROY if env_name == 'dev' else RemovalPolicy.RETAIN,  # 開発環境のみ削除可能
            point_in_time_recovery=True if env_name == 'prod' else False,  # 本番環境のみポイントインタイムリカバリを有効化
        )

