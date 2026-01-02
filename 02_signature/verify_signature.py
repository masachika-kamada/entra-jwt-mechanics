from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
import base64
import json

# 1. 鍵ペアの生成（ホストになったつもり）
# 実際には、この「秘密鍵」はMicrosoftの厳重な金庫の中にあります
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()

print("=== 1. 鍵の準備完了 ===")
print("秘密鍵（誰にも見せない）と公開鍵（みんなに配る）を作りました。\n")

# 2. データの作成
header = {"typ": "JWT", "alg": "RS256"}
payload = {"sub": "1234567890", "name": "John Doe", "admin": False}

# Base64Urlエンコード関数
def base64url_encode(data):
    # JSONを文字列にしてバイト列に変換
    json_bytes = json.dumps(data, separators=(',', ':')).encode('utf-8')
    # Base64エンコードして、URLで使えない文字を置換し、パディング(=)を削除
    return base64.urlsafe_b64encode(json_bytes).rstrip(b'=').decode('utf-8')

encoded_header = base64url_encode(header)
encoded_payload = base64url_encode(payload)

# 署名の対象となるデータ（ヘッダー.ペイロード）
unsigned_token = f"{encoded_header}.{encoded_payload}"

print(f"=== 2. トークンの作成（署名前） ===")
print(f"ヘッダー: {json.dumps(header)}")
print(f"ペイロード: {json.dumps(payload)}")
print(f"署名対象データ: {unsigned_token}\n")

# 3. 署名の作成（秘密鍵を使用）
# ここで「秘密鍵」を使って、署名対象データのハッシュ値を暗号化します
signature = private_key.sign(
    unsigned_token.encode('utf-8'),
    padding.PKCS1v15(),
    hashes.SHA256()
)
# 署名もBase64Urlエンコードします
encoded_signature = base64.urlsafe_b64encode(signature).rstrip(b'=').decode('utf-8')

# 3つをつなげてJWTの完成
jwt = f"{unsigned_token}.{encoded_signature}"

print("=== 3. 署名の作成（秘密鍵を使用） ===")
print(f"生成された署名: {encoded_signature[:20]}...")
print(f"完成したJWT: {jwt}\n")

# 4. 検証（公開鍵を使用）
# サーバー側は「公開鍵」を使って、署名が正しいかチェックします
print("=== 4. 正しいトークンの検証 ===")
try:
    public_key.verify(
        signature,
        unsigned_token.encode('utf-8'),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    print("✅ 検証成功！このトークンは本物です。\n")
except Exception as e:
    print(f"❌ 検証失敗...: {e}\n")

# 5. 改ざん実験
print("=== 5. 改ざん実験（ペイロードを書き換える） ===")
# 悪い人がペイロードを書き換えて「管理者(admin: true)」になろうとしました
fake_payload = {"sub": "1234567890", "name": "John Doe", "admin": True} # adminをTrueに！
encoded_fake_payload = base64url_encode(fake_payload)

# 改ざんされたデータを作成
fake_unsigned_token = f"{encoded_header}.{encoded_fake_payload}"

print(f"改ざん後のペイロード: {json.dumps(fake_payload)}")
print(f"改ざん後の署名対象データ: {fake_unsigned_token}")
print("署名は元のまま（秘密鍵がないので作り直せない）を使います。\n")

# サーバー側での検証
try:
    public_key.verify(
        signature, # 元の署名
        fake_unsigned_token.encode('utf-8'), # 改ざんされたデータ
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    print("✅ 検証成功！...あれ？")
except Exception:
    print("❌ 検証失敗！")
    print("サーバー「署名がデータと一致しません。改ざんされています！」")
    print("-> ペイロードを書き換えても、署名が合わないのでバレました。")
