function handler(event) {
    var request = event.request;
    var headers = request.headers;
    
    // Basic認証の認証情報
    // username: admin
    // password: password123
    // Base64エンコード済み: admin:password123 -> YWRtaW46cGFzc3dvcmQxMjM=
    var authString = 'Basic YWRtaW46cGFzc3dvcmQxMjM=';
    
    // リクエストヘッダーにAuthorizationがあるか確認
    if (
        typeof headers.authorization === 'undefined' ||
        headers.authorization.value !== authString
    ) {
        // 認証失敗: 401 Unauthorizedレスポンスを返す
        return {
            statusCode: 401,
            statusDescription: 'Unauthorized',
            headers: {
                'www-authenticate': { value: 'Basic realm="Secure Area"' }
            }
        };
    }
    
    // 認証成功: リクエストをそのまま通す
    return request;
}

