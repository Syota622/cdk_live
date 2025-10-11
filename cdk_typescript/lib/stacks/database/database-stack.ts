// lib/stacks/database/database-stack.ts
import * as cdk from 'aws-cdk-lib';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import { Construct } from 'constructs';

export interface DatabaseStackProps extends cdk.StackProps {
  environment: string;
  config: any;
}

export class DatabaseStack extends cdk.Stack {
  public readonly userTable: dynamodb.Table;

  constructor(scope: Construct, id: string, props: DatabaseStackProps) {
    super(scope, id, props);

    const { environment, config } = props;

    // User テーブル作成
    this.userTable = new dynamodb.Table(this, 'UserTable', {
      tableName: config.database.tables.user.tableName,
      partitionKey: {
        name: 'userId',
        type: dynamodb.AttributeType.STRING
      },
      billingMode: config.database.tables.user.billingMode === 'PROVISIONED' 
        ? dynamodb.BillingMode.PROVISIONED 
        : dynamodb.BillingMode.PAY_PER_REQUEST,
      readCapacity: config.database.tables.user.readCapacity,
      writeCapacity: config.database.tables.user.writeCapacity,
      removalPolicy: environment === 'prd' 
        ? cdk.RemovalPolicy.RETAIN 
        : cdk.RemovalPolicy.DESTROY,
      pointInTimeRecovery: environment === 'prd',
    });

    // GSI追加（email検索用）
    this.userTable.addGlobalSecondaryIndex({
      indexName: 'EmailIndex',
      partitionKey: {
        name: 'email',
        type: dynamodb.AttributeType.STRING
      },
      projectionType: dynamodb.ProjectionType.ALL,
    });

    // タグ追加
    cdk.Tags.of(this.userTable).add('Environment', environment);
    cdk.Tags.of(this.userTable).add('Project', 'LivestreamHub');

    // 出力
    new cdk.CfnOutput(this, 'UserTableName', {
      value: this.userTable.tableName,
      exportName: `${environment}-UserTableName`
    });

    new cdk.CfnOutput(this, 'UserTableArn', {
      value: this.userTable.tableArn,
      exportName: `${environment}-UserTableArn`
    });
  }
}