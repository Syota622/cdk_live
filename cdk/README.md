# directry
livestream-hub-infrastructure/
├── bin/
│   └── livestream-hub-infrastructure.ts
├── lib/
│   ├── stacks/
│   │   ├── auth/           # Cognito認証スタック
│   │   ├── database/       # DynamoDB関連
│   │   ├── api/           # AppSync API
│   │   ├── storage/       # S3, CloudFront
│   │   └── streaming/     # IVS関連
│   ├── constructs/        # 再利用可能なコンストラクト
│   └── livestream-hub-stack.ts
├── config/
│   ├── dev/              # 開発環境設定
│   ├── qas/              # QA環境設定
│   ├── stg/              # ステージング環境設定
│   └── prd/              # 本番環境設定
├── lambda/
│   ├── resolvers/        # AppSync Resolver
│   └── functions/        # Lambda関数
└── scripts/              # デプロイスクリプト