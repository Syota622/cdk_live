# LiveStreamHub URL設計（AppSync + CloudFront/S3 + IVS）

## 認証（Cognito/Amplify）
- サインアップ: `/signup`
- ログイン: `/login`
- ログアウト: `/logout`
- プロフィール: `/me`
- プロフィール編集: `/me/edit`
- アカウント設定: `/me/settings`
- 通知設定: `/me/notifications/settings`

## ホーム / 検索 / 発見
- ホーム（いま配信中＋近日予定＋新着アーカイブ）: `/`
- ライブ検索: `/search?q=:query&category=:category&sort=:sort`
- チャンネル検索: `/search/channels?q=:query`
- アーカイブ検索: `/search/archives?q=:query`
- カテゴリ別ライブ一覧: `/categories/:category`
- トレンド: `/trending`
- おすすめ: `/recommended`
- チャンネル一覧: `/channels`
- ライブ一覧（全体）: `/lives`
- アーカイブ一覧: `/archives`

## フォロー機能
- フォロー中のチャンネル: `/following`
- フォロー中の配信一覧: `/following/lives`
- フォロワー一覧: `/me/followers`
- フォロー中一覧: `/me/following`

## 通知機能
- 通知一覧: `/notifications`
- 未読通知: `/notifications?unread=true`

## チャンネル
- チャンネル詳細: `/channels/:channelId`
- チャンネル編集（オーナーのみ）: `/channels/:channelId/edit`
- チャンネル内のライブ一覧: `/channels/:channelId/lives`
- チャンネル内のアーカイブ一覧: `/channels/:channelId/archives`
- チャンネル分析（オーナーのみ）: `/channels/:channelId/analytics`
- チャンネルフォロワー一覧: `/channels/:channelId/followers`
- チャンネル設定: `/channels/:channelId/settings`

## ライブ（視聴/詳細/編集）
- ライブ詳細: `/lives/:liveId`
- ライブ視聴ページ（IVS再生UI）: `/lives/:liveId/watch`
- ライブ編集（配信者/オーナー）: `/lives/:liveId/edit`
- ライブ分析（配信者のみ）: `/lives/:liveId/analytics`
- コメント一覧（同一ページ内アンカー）: `/lives/:liveId#comments`
- 配信ガイド（視聴者向けヘルプ）: `/help/watch`

## 配信（配信者向け）
- 配信作成（事前予約）: `/lives/create`
- 配信スケジュール管理: `/lives/schedule`
- 配信のテスト再生ページ（社内/配信者検証用）: `/lives/:liveId/preview`
- 配信ダッシュボード: `/dashboard`
- 配信履歴: `/dashboard/history`
- 配信統計: `/dashboard/analytics`

## アーカイブ
- アーカイブ詳細: `/archives/:archiveId`
- アーカイブ再生: `/archives/:archiveId/watch`
- アーカイブ編集: `/archives/:archiveId/edit`
- アーカイブ分析: `/archives/:archiveId/analytics`

## 管理者機能
- 管理者ダッシュボード: `/admin`
- ユーザー管理: `/admin/users`
- ユーザー詳細: `/admin/users/:userId`
- チャンネル管理: `/admin/channels`
- チャンネル詳細: `/admin/channels/:channelId`
- ライブ管理: `/admin/lives`
- コンテンツモデレーション: `/admin/moderation`
- モデレーションログ: `/admin/moderation/logs`
- システム統計: `/admin/analytics`
- 報告管理: `/admin/reports`

## 運用ヘルスチェック / ステータス
- システムステータス: `/status`
- 視聴トラブルシュート: `/help/troubleshoot`
- 配信トラブルシュート: `/help/streaming`
- パフォーマンス監視: `/status/performance`

## エラーページ
- 404エラー: `/404`
- 500エラー: `/500`
- メンテナンス: `/maintenance`
- アクセス拒否: `/403`

## 法務/その他
- About: `/about`
- 利用規約: `/terms`
- プライバシーポリシー: `/privacy`
- コミュニティガイドライン: `/community-guidelines`
- ヘルプセンター: `/help`
- お問い合わせ: `/contact`
- 採用情報: `/careers`

---

## ネイティブアプリ（配信者：React Native / TestFlight）用ディープリンク
- アプリ起動: `livestreamhub://`
- ログイン: `livestreamhub://login`
- 自分のチャンネル: `livestreamhub://channels/:channelId`
- 配信作成: `livestreamhub://lives/create`
- ライブ編集: `livestreamhub://lives/:liveId/edit`
- **配信開始画面（Go Live）**: `livestreamhub://lives/:liveId/go-live`
- **配信終了処理**: `livestreamhub://lives/:liveId/end`
- 配信ダッシュボード: `livestreamhub://dashboard`
- 通知一覧: `livestreamhub://notifications`
- 設定: `livestreamhub://settings`

> iOSのUniversal Linksを採用する場合は `https://app.example.com/…` に上記をマッピング。

---

## API エンドポイント
> **原則すべてGraphQL（AppSync）経由。**  
> 例外として「署名付きURLの発行」「IVS通知エントリポイント」「管理者API」は API Gateway を利用。

### GraphQL（AppSync）
- GraphQL API: `/api/graphql`
- GraphQL Subscriptions (WebSocket): `/api/graphql-ws`

### RESTful API（API Gateway）
#### 認証・ユーザー管理
- ユーザー登録: `POST /api/auth/register`
- ログイン: `POST /api/auth/login`
- ログアウト: `POST /api/auth/logout`
- トークン更新: `POST /api/auth/refresh`

#### フォロー機能
- チャンネルフォロー: `POST /api/channels/:channelId/follow`
- フォロー解除: `DELETE /api/channels/:channelId/follow`
- フォロー状態確認: `GET /api/channels/:channelId/follow-status`

#### 通知機能
- 通知一覧取得: `GET /api/notifications`
- 通知既読: `PUT /api/notifications/:notificationId/read`
- 通知設定更新: `PUT /api/notifications/settings`

#### 署名付きURL / アセット管理
- **視聴用 CloudFront 署名URL 取得**: `GET /api/playback/:liveId/signed-url`
  - `?expires=300`（有効期限秒）など
- **サムネイル等のS3アップロード用署名URL**: `POST /api/assets/sign`
  - Body: `{ "contentType": "image/jpeg", "keyPrefix": "thumbnails/:liveId" }`
- **アーカイブ用署名URL**: `GET /api/archives/:archiveId/signed-url`

#### 分析・統計
- チャンネル分析データ: `GET /api/analytics/channels/:channelId`
- ライブ分析データ: `GET /api/analytics/lives/:liveId`
- 視聴者統計: `GET /api/analytics/viewers/:liveId`

#### Webhook / イベント処理
- **IVS Webhook/イベント受け口**: `POST /api/webhooks/ivs`
- **録画完了通知**: `POST /api/webhooks/recording-complete`
- **配信状態変更通知**: `POST /api/webhooks/stream-state-change`

#### 管理者API
- システム統計: `GET /api/admin/stats`
- ユーザー管理: `GET /api/admin/users`
- コンテンツモデレーション: `POST /api/admin/moderate`
- レポート処理: `PUT /api/admin/reports/:reportId`

#### 検索・発見
- 詳細検索: `GET /api/search`
  - `?q=query&type=live|channel|archive&category=gaming&sort=popularity`
- トレンド取得: `GET /api/trending`
- おすすめ取得: `GET /api/recommendations/:userId`

---

## 静的アセット（CloudFront/S3）
- React Web アプリ: `/app/*`
- 画像・サムネイル: `/assets/thumbnails/:liveId.jpg`
- チャンネルバナー: `/assets/banners/:channelId.jpg`
- ユーザーアバター: `/assets/avatars/:userId.jpg`
- プレイヤー設定JSON: `/assets/player/:liveId.json`
- アーカイブサムネイル: `/assets/archives/:archiveId.jpg`

---

## URL パラメータ仕様

### 検索パラメータ
- `q`: 検索クエリ
- `category`: カテゴリフィルター（gaming, music, talk, etc.）
- `sort`: ソート順（popularity, recent, viewers, duration）
- `status`: 配信状態（live, scheduled, ended）
- `page`: ページネーション
- `limit`: 表示件数

### フィルタリング例
```
/search?q=ゲーム&category=gaming&sort=viewers&status=live
/lives?category=music&sort=recent&page=2&limit=20
/archives?sort=duration&page=1&limit=50
```

---

## 環境別URL構成

### 本番環境
- Webアプリ: `https://www.livestreamhub.com`
- API: `https://api.livestreamhub.com`
- アセット: `https://cdn.livestreamhub.com`
- 管理者: `https://admin.livestreamhub.com`

### ステージング環境
- Webアプリ: `https://stg.livestreamhub.com`
- API: `https://api-stg.livestreamhub.com`
- アセット: `https://cdn-stg.livestreamhub.com`
- 管理者: `https://admin-stg.livestreamhub.com`

### 開発環境
- Webアプリ: `https://dev.livestreamhub.com`
- API: `https://api-dev.livestreamhub.com`
- アセット: `https://cdn-dev.livestreamhub.com`

---

## セキュリティ考慮事項

1. **レート制限**
   - API呼び出し: 1000req/hour/user
   - 検索API: 100req/hour/user
   - アップロード: 10files/hour/user

2. **CORS設定**
   - 許可ドメイン: 本番・ステージング・開発環境のみ
   - 許可メソッド: GET, POST, PUT, DELETE
   - 認証ヘッダー: Authorization, Content-Type

3. **認証・認可**
   - JWT Bearer Token認証
   - ロールベースアクセス制御（RBAC）
   - API Key認証（管理者API）

### 注意事項
1. `:channelId`、`:liveId`、`:archiveId`、`:userId`、`:query` は動的パラメータです。
2. 実際のルーティングはフロントエンド（React / React Router もしくは Next.js）側で管理します。
3. **データ取得/更新は基本 AppSync の `/api/graphql` を使用**し、コメントやライブ状態など更新通知は **Subscriptions** を利用します。
4. 署名付きURLの発行、分析データ、管理者機能のみ API Gateway エンドポイントを利用します。
5. `#comments` のようなハッシュは同一ページ内セクションへのアンカーを示します。
6. 検索・フィルタリング機能には適切なクエリパラメータを使用します。
7. 管理者機能は別ドメイン（admin.）で分離することでセキュリティを強化します。