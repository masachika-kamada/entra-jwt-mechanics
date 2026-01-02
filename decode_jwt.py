import base64
import json
import sys

# アクセストークンが書かれたファイルを読み込む
try:
    with open('access_token', 'r', encoding='utf-8') as f:
        token = f.read().strip()
except FileNotFoundError:
    print("エラー: 'access_token' というファイルが見つかりません。")
    sys.exit(1)

def decode_base64_url(data):
    """Base64Url文字列をデコードする関数"""
    # パディング（=）が足りない場合は補完する
    padding = '=' * (4 - len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)

# ドットで3つの部分に分割する
parts = token.split('.')

if len(parts) == 3:
    header = parts[0]
    payload = parts[1]
    signature = parts[2]

    print("--- 1. ヘッダー (Header) ---")
    try:
        header_bytes = decode_base64_url(header)
        print(header_bytes.decode('utf-8'))
    except Exception as e:
        print(f"ヘッダーのデコードに失敗しました: {e}")

    print("\n--- 2. ペイロード (Payload: 中身) ---")
    try:
        payload_bytes = decode_base64_url(payload)
        # JSONとしてきれいに表示
        payload_str = payload_bytes.decode('utf-8')
        payload_json = json.loads(payload_str)
        print(json.dumps(payload_json, indent=2, ensure_ascii=False))
    except UnicodeDecodeError:
        print("デコードエラー: ペイロードが正しいUTF-8テキストではありません。")
    except json.JSONDecodeError:
        print("JSONエラー: ペイロードが正しいJSON形式ではありません。")
    except Exception as e:
        print(f"ペイロードのデコードに失敗しました: {e}")

    print("\n--- 3. 署名 (Signature) ---")
    print("※署名はバイナリデータ（暗号化されたハッシュ値）なので、デコードして使用するものではないです。")
    print(f"署名の長さ: {len(signature)} 文字")

else:
    print(f"エラー: トークンの形式が正しくありません。")
    print(f"期待される形式: ヘッダー.ペイロード.署名 (ドットで3つに区切られている)")
    print(f"実際の区切り数: {len(parts)}")
