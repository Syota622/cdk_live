# Basic認証について

## 認証情報

CloudFrontのBasic認証には以下の認証情報を使用してください：

```
ユーザー名: admin
パスワード: password123
```

## 適用環境

- **開発環境 (dev)**: Basic認証有効
- **ステージング環境 (stg)**: Basic認証有効
- **本番環境 (prod)**: Basic認証無効

## 認証情報の変更方法

認証情報を変更する場合は、以下の手順で行ってください：

### 1. 新しい認証情報をBase64エンコード

ターミナルで以下のコマンドを実行：

```bash
# macOS/Linux
echo -n "username:password" | base64

# 例: admin:newpassword の場合
echo -n "admin:newpassword" | base64
# 結果: YWRtaW46bmV3cGFzc3dvcmQ=
```

### 2. basic_auth.jsを編集

`lib/cdk/cloudfront/basic_auth.js`

```javascript
// Base64エンコード済みの認証文字列に変更
var authString = 'Basic YWRtaW46cGFzc3dvcmQxMjM=';  // ← ここを変更
```

### 3. 再デプロイ

```bash
cdk deploy DevStack
```

## Basic認証の有効/無効の切り替え

`lib/cdk/common_stack.py` で環境ごとに設定できます：

```python
# 開発・ステージング環境はBasic認証を有効化、本番環境は無効化
enable_basic_auth = env_name in ['dev', 'stg']
```

特定の環境でBasic認証を無効にする場合：

```python
# すべての環境でBasic認証を無効化
enable_basic_auth = False

# または特定の環境のみ有効化
enable_basic_auth = env_name == 'dev'  # 開発環境のみ
```

## 注意事項

- Basic認証はCloudFront Functionsで実装されています
- 認証情報はコードにハードコーディングされています（本番環境では推奨されません）
- より安全な方法として、Secrets ManagerやParameter Storeの使用を検討してください
- CloudFrontのキャッシュがあるため、変更が反映されるまで数分かかる場合があります

