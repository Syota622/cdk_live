# LiveStreamHub 開発ロードマップ

## 🎯 Phase 0: プロジェクト準備・環境構築（推定：3-5日）

### ステップ1: プロジェクト初期化
**優先度:** 最高 | **工数:** 1日

#### 今すぐ始めること
1. **GitHubリポジトリ作成**
   ```bash
   # フロントエンド
   create-react-app livestream-frontend
   cd livestream-frontend
   git init && git remote add origin <your-repo>
   
   # バックエンド用リポジトリも作成
   mkdir livestream-backend && cd livestream-backend
   git init && git remote add origin <your-backend-repo>
   ```

2. **開発環境セットアップ**
   ```bash
   # 必要ツールのインストール
   npm install -g @aws-amplify/cli
   npm install -g aws-cdk
   aws configure  # AWSクレデンシャル設定
   ```

3. **プロジェクト構造作成**
   ```
   livestream-hub/
   ├── frontend/          # React アプリ
   ├── backend/           # CDK/Lambda
   ├── mobile/            # React Native (後で)
   ├── docs/              # ドキュメント
   └── scripts/           # デプロイスクリプト
   ```

---

### ステップ2: AWS基盤構築
**優先度:** 最高 | **工数:** 2日

#### 作業内容
1. **Amplify初期化**
   ```bash
   cd frontend
   amplify init
   # プロジェクト名: livestream-hub
   # 環境: dev
   ```

2. **認証設定**
   ```bash
   amplify add auth
   # 設定: Email/Password, MFA無効
   amplify push
   ```

3. **基本的なDynamoDBテーブル作成**
   ```bash
   amplify add storage
   # NoSQL Database選択
   # テーブル: User, Channel, Live (最小構成)
   ```

#### 受入条件
- [ ] AWS環境が正常に動作
- [ ] Cognitoでユーザー登録・ログインが可能
- [ ] 基本テーブルが作成済み

---

## 🏗️ Phase 1: MVP基盤構築（推定：7-10日）

### ステップ3: 認証機能実装
**優先度:** 最高 | **工数:** 3日

#### フロントエンド実装
```javascript
// src/App.js
import { Authenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';

function App() {
  return (
    <Authenticator>
      {({ signOut, user }) => (
        <main>
          <h1>Welcome {user.username}</h1>
          <button onClick={signOut}>Sign out</button>
        </main>
      )}
    </Authenticator>
  );
}
```

#### 実装項目
- [x] ログイン・サインアップページ
- [x] プロフィール表示
- [x] 認証状態管理
- [x] ルート保護機能

---

### ステップ4: GraphQL API構築
**優先度:** 最高 | **工数:** 4日

#### AppSync API追加
```bash
amplify add api
# GraphQL選択
# 認証タイプ: Amazon Cognito User Pool
```

#### 最小限のスキーマ定義
```graphql
type User @model @auth(rules: [{allow: owner}]) {
  id: ID!
  name: String!
  email: String!
  avatarUrl: String
  createdAt: AWSDateTime!
}

type Channel @model @auth(rules: [{allow: owner}]) {
  id: ID!
  name: String!
  description: String
  ownerId: ID!
  createdAt: AWSDateTime!
}

type Live @model {
  id: ID!
  title: String!
  channelId: ID!
  status: String!
  createdAt: AWSDateTime!
}
```

#### 受入条件
- [ ] GraphQL APIが正常に動作
- [ ] 基本的なCRUD操作が可能
- [ ] 認証連携が動作

---

## 🎪 Phase 2: ライブ配信基本機能（推定：8-12日）

### ステップ5: IVS設定・配信機能
**優先度:** 最高 | **工数:** 5日

#### 手動でIVS設定
1. **AWS IVSコンソールでチャンネル作成**
2. **ストリームキー取得**
3. **HLS再生URL取得**

#### フロントエンド実装
```javascript
// ライブ作成ページ
const CreateLive = () => {
  const [title, setTitle] = useState('');
  
  const handleCreate = async () => {
    // GraphQL mutation でライブ作成
    const result = await API.graphql({
      query: createLive,
      variables: { input: { title, channelId: userChannelId } }
    });
  };
};
```

#### 受入条件
- [ ] ライブ配信作成機能
- [ ] 基本的な視聴機能
- [ ] 配信状態管理

---

### ステップ6: 視聴ページ実装
**優先度:** 高 | **工数:** 3日

#### HLS.js統合
```javascript
// 視聴ページコンポーネント
import Hls from 'hls.js';

const WatchLive = ({ liveId }) => {
  useEffect(() => {
    const video = videoRef.current;
    const hls = new Hls();
    hls.loadSource(hlsUrl);
    hls.attachMedia(video);
  }, [hlsUrl]);
};
```

---

## 🗨️ Phase 3: リアルタイム機能（推定：5-7日）

### ステップ7: リアルタイムコメント
**優先度:** 高 | **工数:** 4日

#### GraphQL Subscription
```graphql
type Comment @model {
  id: ID!
  content: String!
  liveId: ID!
  userId: ID!
  createdAt: AWSDateTime!
}

type Subscription {
  onCreateComment(liveId: ID!): Comment
    @aws_subscribe(mutations: ["createComment"])
}
```

#### 受入条件
- [ ] リアルタイムコメント投稿
- [ ] コメント一覧表示
- [ ] Subscription動作確認

---

## 📱 Phase 4: UI/UX改善（推定：5-8日）

### ステップ8: レスポンシブUI実装
**優先度:** 中 | **工数:** 5日

#### Tailwind CSS導入
```bash
npm install tailwindcss @tailwindcss/forms
npx tailwindcss init
```

#### 主要ページデザイン
- ホームページ
- チャンネル一覧
- ライブ視聴ページ
- 配信作成ページ

---

## 🚀 Phase 5: デプロイ・テスト（推定：3-5日）

### ステップ9: 本番デプロイ
**優先度:** 高 | **工数:** 3日

#### Amplifyホスティング
```bash
amplify add hosting
# Hosting with Amplify Console選択
amplify publish
```

#### 受入条件
- [ ] 本番環境でのテスト完了
- [ ] SSL証明書設定
- [ ] ドメイン設定

---

## 📋 最初の1週間で取り組むべきタスク

### Day 1: 環境構築
- [ ] AWSアカウント・GitHub準備
- [ ] Amplify CLI設定
- [ ] プロジェクト作成

### Day 2-3: 認証実装
- [ ] Cognito設定
- [ ] ログイン・サインアップ画面
- [ ] 認証フロー確認

### Day 4-5: API基盤
- [ ] GraphQL API作成
- [ ] 基本スキーマ定義
- [ ] CRUD操作確認

### Day 6-7: 最初のライブ機能
- [ ] IVS手動設定
- [ ] ライブ作成機能
- [ ] 基本視聴機能

---

## ⚡ 今日から始められること

### 即座に実行可能なタスク

1. **AWSアカウント確認**
   - 既存アカウントの権限確認
   - 必要であれば新規作成

2. **開発環境準備**
   ```bash
   # Node.js最新版インストール
   # Git設定確認
   # VS Code + AWS Toolkit拡張インストール
   ```

3. **GitHubリポジトリ作成**
   - フロントエンド用リポジトリ
   - バックエンド用リポジトリ
   - Issue templateやPRテンプレート設定

4. **技術検証**
   - Amplify CLIインストール・設定
   - 簡単なReactアプリ作成
   - AWS IVSコンソール確認

---

## 🎯 成功指標（各フェーズ終了時）

### Phase 0 完了時
- AWS環境が動作し、Amplify CLIが使用可能

### Phase 1 完了時  
- ユーザー登録・ログインが動作
- GraphQL APIで基本的なデータ操作が可能

### Phase 2 完了時
- ライブ配信作成・視聴が基本的に動作

### Phase 3 完了時
- リアルタイムコメントが動作

### Phase 4 完了時
- 実用的なUIでMVPとして使用可能

### Phase 5 完了時
- 本番環境でのライブ配信プラットフォームが稼働

---

## 🚨 リスク・注意点

1. **IVS料金**
   - 開発時は最小構成で開始
   - 不要なチャンネルは削除

2. **Amplify制限**
   - 無料枠の確認
   - DynamoDB使用量監視

3. **技術的負債**
   - 早期は手動設定で進める
   - 後でIaC（CDK）化を検討

**最初の一歩**: まずはAWS環境の準備とGitHubリポジトリ作成から始めましょう！