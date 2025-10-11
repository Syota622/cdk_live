# API Gateway with AWS CDK (Python)

AWS CDK (Python)を使用したシンプルなREST API Gatewayのプロジェクトです。

## プロジェクト構成

```
.
├── app.py                      # CDKアプリケーションのエントリーポイント
├── lib/                        # メインのコード格納フォルダ
│   ├── cdk/                   # CDKスタック定義
│   │   ├── __init__.py
│   │   └── api_gateway_stack.py  # API Gateway + Lambda スタック
│   ├── lambda/                # Lambda関数
│   │   └── handler.py         # API用Lambda関数
│   └── README.md              # libフォルダの説明
├── requirements.txt           # Python依存関係
└── README.md                  # このファイル
```

## 構築されるリソース

- **Lambda関数**: API Gatewayからのリクエストを処理
- **API Gateway REST API**: 以下のエンドポイントを提供
  - `GET /hello` - シンプルなHelloエンドポイント
  - `GET /items` - アイテム一覧取得
  - `POST /items` - アイテム作成
  - `GET /items/{id}` - 特定アイテム取得
  - `PUT /items/{id}` - アイテム更新
  - `DELETE /items/{id}` - アイテム削除

## セットアップ

### 1. 仮想環境の作成と有効化

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windowsの場合: .venv\Scripts\activate.bat
```

### 2. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 3. CDKのブートストラップ（初回のみ）

```bash
cdk bootstrap
```

## デプロイ

### CloudFormationテンプレートの合成

```bash
cdk synth
```

### スタックのデプロイ

```bash
cdk deploy
```

デプロイが完了すると、API GatewayのエンドポイントURLが出力されます。

## 使い方

デプロイ後、出力されたAPIエンドポイントURLを使用してテスト:

```bash
# Helloエンドポイント
curl https://YOUR_API_ID.execute-api.REGION.amazonaws.com/prod/hello

# Itemsエンドポイント
curl https://YOUR_API_ID.execute-api.REGION.amazonaws.com/prod/items
```

## CDK便利コマンド

* `cdk ls` - スタック一覧表示
* `cdk synth` - CloudFormationテンプレートを合成
* `cdk deploy` - AWSアカウント/リージョンにスタックをデプロイ
* `cdk diff` - デプロイ済みスタックと現在の状態を比較
* `cdk destroy` - スタックを削除
* `cdk docs` - CDKドキュメントを開く

## カスタマイズ

### Lambda関数の編集
Lambda関数のロジックは `lib/lambda/handler.py` で編集できます。

### CDKスタックの編集
API Gatewayのエンドポイントやリソース設定は `lib/cdk/api_gateway_stack.py` で追加/変更できます。

### 新しいスタックの追加
1. `lib/cdk/` に新しいスタックファイルを作成
2. `app.py` でインポートしてインスタンス化
