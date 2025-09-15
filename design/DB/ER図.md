```mermaid
erDiagram

  direction LR

  USER {
    string userId_PK
    string name
    string email
    string avatarUrl
    datetime createdAt
  }

  CHANNEL {
    string channelId_PK
    string ownerId_FK
    string name
    string description
    datetime createdAt
    datetime updatedAt
  }

  LIVE {
    string liveId_PK
    string channelId_FK
    string title
    string description
    string status
    string ivsChannelArn
    string thumbnailUrl
    datetime startTime
    datetime endTime
    datetime createdAt
    datetime updatedAt
  }

  COMMENT {
    string liveId_PK
    string commentId_SK
    string userId_FK
    string content
    datetime createdAt
  }

  ARCHIVE {
    string archiveId_PK
    string liveId_FK
    string s3Url
    int duration
    datetime createdAt
  }

  LIKE {
    string targetId_PK
    string userId_SK
    string targetType
    datetime createdAt
  }

  USER ||--o{ CHANNEL : owns
  CHANNEL ||--o{ LIVE : hosts
  LIVE ||--o{ COMMENT : has
  LIVE }o--|| ARCHIVE : produces
  LIVE ||--o{ LIKE : receives
  COMMENT ||--o{ LIKE : receives


```