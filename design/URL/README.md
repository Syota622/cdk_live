# LiveStreamHub URL設計（AppSync + CloudFront/S3 + IVS）

## 認証（Cognito/Amplify）
- サインアップ: `/signup`
- ログイン: `/login`
- ログアウト: `/logout`
- プロフィール: `/me`
- プロフィール編集: `/me/edit`

## ホーム / 検索
- ホーム（いま配信中＋近日予定＋新着アーカイブ）: `/`
- ライブ検索: `/search?q=:query`
- チャンネル一覧: `/channels`
- ライブ一覧（全体）: `/lives`
- アーカイブ一覧: `/archives`

## チャンネル
- チャンネル詳細: `/channels/:channelId`
- チャンネル編集（オーナーのみ）: `/channels/:channelId/edit`
- チャンネル内のライブ一覧: `/channels/:channelId/lives`

## ライブ（視聴/詳細/編集）
- ライブ詳細: `/lives/:liveId`
- ライブ視聴ページ（IVS再生UI）: `/lives/:liveId/watch`
- ライブ編集（配信者/オーナー）: `/lives/:liveId/edit`
- コメント一覧（同一ページ内アンカー）: `/lives/:liveId#comments`
- 配信ガイド（視聴者向けヘルプ）: `/help/watch`

## 配信（配信者向け）
- 配信作成（事前予約）: `/lives/create`
- 配信のテスト再生ページ（社内/配信者検証用）: `/lives/:liveId/preview`  
  ※本番配信は ReactNative アプリから実施（下記ディープリンク参照）

## アーカイブ
- アーカイブ詳細: `/archives/:archiveId`
- アーカイブ再生: `/archives/:archiveId/watch`

## 運用ヘルスチェック / ステータス
- システムステータス: `/status`
- 視聴トラブルシュート: `/help/troubleshoot`

## 法務/その他
- About: `/about`
- 利用規約: `/terms`
- プライバシーポリシー: `/privacy`

---

## ネイティブアプリ（配信者：React Native / TestFlight）用ディープリンク
- アプリ起動: `livestreamhub://`
- ログイン: `livestreamhub://login`
- 自分のチャンネル: `livestreamhub://channels/:channelId`
- 配信作成: `livestreamhub://lives/create`
- ライブ編集: `livestreamhub://lives/:liveId/edit`
- **配信開始画面（Go Live）**: `livestreamhub://lives/:liveId/go-live`
- **配信終了処理**: `livestreamhub://lives/:liveId/end`

> iOSのUniversal Linksを採用する場合は `https://app.example.com/…` に上記をマッピング。

---

## API エンドポイント
> **原則すべてGraphQL（AppSync）経由。**  
> 例外として「署名付きURLの発行」「IVS通知エントリポイント」は API Gateway を利用。

### GraphQL（AppSync）
- GraphQL API: `/api/graphql`
- GraphQL Subscriptions (WebSocket): `/api/graphql-ws`

### 署名付きURL / 周辺ユースケース（API Gateway）
- **視聴用 CloudFront 署名URL 取得**: `GET /api/playback/:liveId/signed-url`
  - `?expires=300`（有効期限秒）など
- **サムネイル等のS3アップロード用署名URL**: `POST /api/assets/sign`
  - Body: `{ "contentType": "image/jpeg", "keyPrefix": "thumbnails/:liveId" }`
- **IVS Webhook/イベント受け口（EventBridge → APIGW想定）**: `POST /api/webhooks/ivs`
  - 録画完了・配信状態変化を受信してアーカイブ登録等をトリガー

---

## 静的アセット（CloudFront/S3）
- React Web アプリ: `/app/*`
- 画像・サムネイル: `/assets/thumbnails/:liveId.jpg`
- プレイヤー設定JSON: `/assets/player/:liveId.json`

---

### 注意事項
1. `:channelId`、`:liveId`、`:archiveId`、`:query` は動的パラメータです。  
2. 実際のルーティングはフロントエンド（React / React Router もしくは Next.js）側で管理します。  
3. **データ取得/更新は基本 AppSync の `/api/graphql` を使用**し、コメントやライブ状態など更新通知は **Subscriptions** を利用します。  
4. 署名付きURLの発行のみ API Gateway エンドポイントを利用します（視聴HLS URLやS3直アクセスの保護目的）。  
5. `#comments` のようなハッシュは同一ページ内セクションへのアンカーを示します。  
6. 環境ごとにベースURLを分けます（例）  
   - 本番: `https://www.example.com`  
   - ステージング: `https://stg.example.com`  
   - API（共通パス）: `https://api.example.com`（`/api/graphql` / `/api/*` がぶら下がる）
