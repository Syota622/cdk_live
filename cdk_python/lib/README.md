# lib フォルダ

このフォルダには、CDKスタックとLambda関数のコードを管理します。

## 構造

```
lib/
├── cdk/                       # CDKスタック定義
│   ├── __init__.py
│   └── api_gateway_stack.py  # API Gateway + Lambda スタック
└── lambda/                    # Lambda関数
    └── handler.py            # API Gateway用のLambda関数
```

## cdk/

CDKスタックの定義を格納するフォルダです。

### api_gateway_stack.py

API Gateway と Lambda 関数を定義するCDKスタックです。

**作成されるリソース:**
- Lambda関数: `ApiHandler`
- API Gateway REST API: `SimpleApi`
- エンドポイント: `/hello`, `/items`, `/items/{id}`

**カスタマイズポイント:**
- Lambda関数の設定（メモリ、タイムアウトなど）
- API Gatewayのエンドポイント追加/変更
- CORSやカスタムドメインの設定

## lambda/

Lambda関数のコードを格納するフォルダです。

### handler.py

API Gatewayからのリクエストを処理するLambda関数です。

**機能:**
- HTTPメソッドとパスを取得
- JSONレスポンスを返却
- CORS対応のヘッダーを設定

**カスタマイズポイント:**
- ビジネスロジックの実装
- データベース連携
- エラーハンドリング
