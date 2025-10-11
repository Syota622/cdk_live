// bin/livestream-hub-infrastructure.ts
#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { DatabaseStack } from '../lib/stacks/database/database-stack';
import * as fs from 'fs';
import * as path from 'path';

const app = new cdk.App();

// CDK Contextから環境名を取得（デフォルトはdev）
const environment = app.node.tryGetContext('environment') || 'dev';

// 設定ファイル読み込み
const configPath = path.join(__dirname, '..', 'config', environment, 'config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

console.log(`Deploying to environment: ${environment}`);
console.log(`Using AWS Profile: ${config.profile}`);
console.log(`Target Account: ${config.accountId}`);

// スタック作成
const databaseStack = new DatabaseStack(app, `LivestreamHub-Database-${environment}`, {
  environment,
  config,
  env: {
    account: config.accountId,
    region: config.region,
  },
  description: `LivestreamHub Database Stack for ${environment} environment`
});

// タグ追加
cdk.Tags.of(app).add('Project', 'LivestreamHub');
cdk.Tags.of(app).add('Environment', environment);