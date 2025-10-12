from aws_cdk import Stack, CfnOutput
from constructs import Construct

from .lambda_function.mobile.get.app import ApiLambdaConstruct
from .api_gateway.mobile.api_gateway import ApiGatewayConstruct
from .dynamodb.dynamodb import DynamoDBConstruct
from .s3.s3 import S3Construct
from .cloudfront.cloudfront import CloudFrontConstruct


class ApiGatewayStack(Stack):
    """
    フルスタックアプリケーションのCDKスタック

    このスタックは以下のリソースを作成します:
    - S3: フロントエンドの静的ファイルをホスティング
    - CloudFront: CDNでフロントエンドを配信
    - DynamoDB: データストレージ
    - Lambda関数: API Gatewayからのリクエストを処理
    - API Gateway REST API: RESTful APIエンドポイントを提供
    
    リファクタリングにより、各リソースは独立したコンストラクトとして管理されています。
    
    フォルダ構造:
        cdk/
            common_stack.py                 (このファイル)
            s3/
                s3.py                       (S3構築)
            cloudfront/
                cloudfront.py               (CloudFront構築)
            dynamodb/
                dynamodb.py                 (DynamoDB構築)
            lambda_function/
                mobile/
                    get/
                        app.py              (Lambda構築)
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

        # S3バケットの作成
        s3_construct = S3Construct(
            self, "S3Construct",
            pj_name=pj_name,
            env_name=env_name
        )

        # CloudFrontディストリビューションの作成
        cloudfront_construct = CloudFrontConstruct(
            self, "CloudFrontConstruct",
            pj_name=pj_name,
            env_name=env_name,
            frontend_bucket=s3_construct.frontend_bucket
        )

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
            hello_table=dynamodb_construct.hello_table,
            items_table=dynamodb_construct.items_table
        )

        # API Gatewayの作成
        api_gateway_construct = ApiGatewayConstruct(
            self, "ApiGatewayConstruct",
            pj_name=pj_name,
            env_name=env_name,
            lambda_function=mobile_hello_get.function
        )

        # 作成されたリソースへの参照を保持
        self.frontend_bucket = s3_construct.frontend_bucket
        self.cloudfront_distribution = cloudfront_construct.distribution
        self.hello_table = dynamodb_construct.hello_table
        self.items_table = dynamodb_construct.items_table
        self.lambda_function = mobile_hello_get.function
        self.api = api_gateway_construct.api

        # CloudFormationの出力
        CfnOutput(
            self, "CloudFrontURL",
            value=f"https://{cloudfront_construct.domain_name}",
            description="CloudFront Distribution URL"
        )

        CfnOutput(
            self, "ApiGatewayURL",
            value=api_gateway_construct.api.url,
            description="API Gateway URL"
        )

        CfnOutput(
            self, "S3BucketName",
            value=s3_construct.frontend_bucket.bucket_name,
            description="Frontend S3 Bucket Name"
        )
