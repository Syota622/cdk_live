#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { LiveStreamHubStack } from '../lib/livestream-hub-stack';
import * as fs from 'fs';
import * as path from 'path';

// 環境変数から環境を取得（デフォルトはdev）
const environment = process.env.ENVIRONMENT || 'dev';

// 設定ファイル読み込み
const configPath = path.join(__dirname, `../config/${environment}/config.json`);
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

const app = new cdk.App();

new LiveStreamHubStack(app, `${config.stackPrefix}-Stack`, {
  env: {
    account: config.account,
    region: config.region,
  },
  environment: config.environment,
  projectName: config.projectName,
  stackPrefix: config.stackPrefix
});