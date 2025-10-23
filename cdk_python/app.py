#!/usr/bin/env python3
import os
import sys

import aws_cdk as cdk

# libフォルダをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from cdk.common_stack import CommonStack


app = cdk.App()

# 開発環境のスタック
CommonStack(
    app, "DevStack",
    pj_name='livestream',
    env_name='dev',
    env=cdk.Environment(
        account='235484765172',  # 自分のAWSアカウントIDに変更
        region='ap-northeast-1'
    ),
)

# ステージング環境のスタック
CommonStack(
    app, "StgStack",
    pj_name='livestream',
    env_name='stg',
    env=cdk.Environment(
        account='123456789012',  # 自分のAWSアカウントIDに変更
        region='ap-northeast-1'
    ),
)

# 本番環境のスタック
CommonStack(
    app, "ProdStack",
    pj_name='livestream',
    env_name='prod',
    env=cdk.Environment(
        account='123456789012',  # 自分のAWSアカウントIDに変更
        region='ap-northeast-1'
    ),
)

app.synth()
