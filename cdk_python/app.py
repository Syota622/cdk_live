#!/usr/bin/env python3
import os
import sys

import aws_cdk as cdk

# libフォルダをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from cdk.common_stack import ApiGatewayStack


app = cdk.App()

# プロジェクト名を取得（コンテキストまたはデフォルト値）
# cdk deploy DevStack -c pj_name=myproject のように指定可能
pj_name = app.node.try_get_context('pj_name') or 'livestream'

# 開発環境のスタック
ApiGatewayStack(
    app, "DevStack",
    pj_name=pj_name,
    env_name='dev',
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    ),
)

# ステージング環境のスタック
ApiGatewayStack(
    app, "StgStack",
    pj_name=pj_name,
    env_name='stg',
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    ),
)

# 本番環境のスタック
ApiGatewayStack(
    app, "ProdStack",
    pj_name=pj_name,
    env_name='prod',
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    ),
)

app.synth()
