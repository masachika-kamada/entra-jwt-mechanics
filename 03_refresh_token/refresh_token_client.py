import requests
import json
import sys
import os
from dotenv import load_dotenv

# .env ファイルを同じディレクトリから読み込む
load_dotenv()

TOKEN_FILE = 'refresh_token.txt'

def get_config():
    """環境変数から設定を読み込む"""
    tenant_id = os.getenv('TENANT_ID')
    client_id = os.getenv('CLIENT_ID')
    scope = os.getenv('SCOPE')
    origin = os.getenv('ORIGIN')

    if not tenant_id or not client_id:
        print("エラー: 環境変数が設定されていません。")
        print("プロジェクトルートの .env ファイルを確認してください。")
        sys.exit(1)

    return {
        "tenant_id": tenant_id,
        "client_id": client_id,
        "scope": scope,
        "origin": origin
    }

def load_refresh_token():
    """リフレッシュトークンをファイルから読み込む"""
    if not os.path.exists(TOKEN_FILE):
        print(f"エラー: '{TOKEN_FILE}' ファイルが見つかりません。")
        print(f"ブラウザからコピーしたリフレッシュトークンを '{TOKEN_FILE}' に保存してください。")
        sys.exit(1)
    
    with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
        return f.read().strip()

def save_refresh_token(token):
    """新しいリフレッシュトークンをファイルに保存する"""
    with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
        f.write(token)
    print(f"💾 新しいリフレッシュトークンを '{TOKEN_FILE}' に保存しました。")

def refresh_access_token():
    config = get_config()
    refresh_token = load_refresh_token()
    
    # Microsoft Entra ID のトークンエンドポイント
    url = f"https://login.microsoftonline.com/{config['tenant_id']}/oauth2/v2.0/token"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # SPAの場合はOriginヘッダーが必要
    if config.get('origin'):
        headers['Origin'] = config['origin']
    
    # 更新リクエストのデータ
    data = {
        "client_id": config['client_id'],
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    
    # スコープが指定されていれば追加
    if config.get('scope'):
        data['scope'] = config['scope']

    print(f"--- リクエスト送信中 ---")
    print(f"URL: {url}")
    print(f"Client ID: {config['client_id']}")
    
    try:
        response = requests.post(url, headers=headers, data=data)
        
        print(f"\n--- レスポンス (Status: {response.status_code}) ---")
        
        if response.status_code == 200:
            result = response.json()
            print("\n=== 更新結果の確認 ===")
            
            # 1. アクセストークン
            print(f"✅ アクセストークン: 新しく発行されました (有効期限: {result.get('expires_in')} 秒)")
            new_access_token = result.get('access_token', '')
            print(f"   Value: {new_access_token[:20]}...")

            # 2. リフレッシュトークン
            new_refresh_token = result.get('refresh_token')
            if new_refresh_token:
                if new_refresh_token != refresh_token:
                    print("✅ リフレッシュトークン: 新しい値に更新されました (ローテーション)")
                    print(f"   Old: {refresh_token[:20]}...{refresh_token[-10:]}")
                    print(f"   New: {new_refresh_token[:20]}...{new_refresh_token[-10:]}")
                    
                    # 新しいトークンを保存
                    save_refresh_token(new_refresh_token)
                else:
                    print("ℹ️ リフレッシュトークン: 値は変わりませんでした")
            else:
                print("ℹ️ リフレッシュトークン: レスポンスに含まれていませんでした")
        else:
            print("❌ 失敗...")
            print(json.dumps(response.json(), indent=2))
            
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    refresh_access_token()
