from aws_cdk import (
    aws_ivs as ivs,
    aws_s3 as s3,
)
from constructs import Construct


class IVSConstruct(Construct):
    """
    Amazon IVS (Interactive Video Service) を構築するコンストラクト
    
    ライブ配信用のチャンネルとストリームキーを作成します。
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        pj_name: str,
        env_name: str,
        recording_bucket: s3.Bucket = None,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # IVS チャンネルの作成
        # テスト段階のため、STANDARDタイプを使用（低コスト）
        self.channel = ivs.CfnChannel(
            self, "LiveStreamChannel",
            name=f"{pj_name}-{env_name}-live-channel",
            type="STANDARD",  # STANDARD または BASIC
            latency_mode="LOW",  # LOW または NORMAL
            authorized=False,  # 認証なし（テスト用）
        )

        # ストリームキーの作成
        self.stream_key = ivs.CfnStreamKey(
            self, "StreamKey",
            channel_arn=self.channel.attr_arn,
        )

        # 録画設定（オプション：本番環境のみ有効化）
        if recording_bucket and env_name == 'prod':
            recording_configuration = ivs.CfnRecordingConfiguration(
                self, "RecordingConfiguration",
                name=f"{pj_name}-{env_name}-recording",
                destination_configuration=ivs.CfnRecordingConfiguration.DestinationConfigurationProperty(
                    s3=ivs.CfnRecordingConfiguration.S3DestinationConfigurationProperty(
                        bucket_name=recording_bucket.bucket_name
                    )
                ),
            )
            
            # チャンネルに録画設定を関連付け
            # Note: CDKではチャンネル作成後に録画設定を更新する必要があります
            # この部分は手動で設定するか、カスタムリソースを使用します

        # プレイバック情報を保持
        self.playback_url = self.channel.attr_playback_url
        self.ingest_endpoint = self.channel.attr_ingest_endpoint
        self.channel_arn = self.channel.attr_arn

