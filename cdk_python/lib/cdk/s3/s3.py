from aws_cdk import (
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    RemovalPolicy,
)
from constructs import Construct
import os


class S3Construct(Construct):
    """
    S3バケットを構築するコンストラクト
    
    フロントエンド用の静的ファイルをホスティングするS3バケットを作成します。
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

        # フロントエンド用S3バケットの作成
        self.frontend_bucket = s3.Bucket(
            self, "FrontendBucket",
            bucket_name=f"{pj_name}-{env_name}-frontend",
            versioned=True,  # バージョニング有効化
            encryption=s3.BucketEncryption.S3_MANAGED,  # サーバーサイド暗号化
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,  # パブリックアクセスをブロック（CloudFront経由のみ）
            removal_policy=RemovalPolicy.DESTROY if env_name == 'dev' else RemovalPolicy.RETAIN,
            auto_delete_objects=True if env_name == 'dev' else False,  # 開発環境のみ自動削除
        )

        # フロントエンドファイルのデプロイ
        # プロジェクトルートのfrontendフォルダからデプロイ
        frontend_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "..", "frontend"
        )
        
        self.deployment = s3deploy.BucketDeployment(
            self, "DeployFrontend",
            sources=[s3deploy.Source.asset(frontend_path)],
            destination_bucket=self.frontend_bucket,
            prune=True,  # 不要なファイルを削除
        )

