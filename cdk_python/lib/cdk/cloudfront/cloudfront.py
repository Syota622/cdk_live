from aws_cdk import (
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_s3 as s3,
    Duration,
)
from constructs import Construct


class CloudFrontConstruct(Construct):
    """
    CloudFrontディストリビューションを構築するコンストラクト
    
    S3バケットをオリジンとするCDNを作成します。
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        pj_name: str,
        env_name: str,
        frontend_bucket: s3.Bucket,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Origin Access Identity (OAI)を作成
        # CloudFrontからS3へのアクセスを許可
        oai = cloudfront.OriginAccessIdentity(
            self, "OAI",
            comment=f"{pj_name}-{env_name} OAI for frontend"
        )

        # S3バケットにOAIへの読み取り権限を付与
        frontend_bucket.grant_read(oai)

        # CloudFrontディストリビューションの作成
        self.distribution = cloudfront.Distribution(
            self, "Distribution",
            comment=f"{pj_name}-{env_name} CloudFront Distribution",
            default_root_object="index.html",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(
                    frontend_bucket,
                    origin_access_identity=oai
                ),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD,
                cached_methods=cloudfront.CachedMethods.CACHE_GET_HEAD,
                cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
                compress=True,
            ),
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=Duration.minutes(5)
                ),
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=Duration.minutes(5)
                )
            ],
            price_class=cloudfront.PriceClass.PRICE_CLASS_200,  # 北米、欧州、アジア、中東、アフリカ
        )

        # CloudFrontのドメイン名を出力用に保持
        self.domain_name = self.distribution.distribution_domain_name

