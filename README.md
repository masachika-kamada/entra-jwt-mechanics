# Entra JWT Mechanics

このリポジトリは、Microsoft Entra ID (旧 Azure AD) のアクセストークンや JWT (JSON Web Token) の仕組みについて学習した内容と、検証用コードをまとめたものです。
アクセストークンの内部構造、Base64エンコードのビット計算、RSA署名による改ざん防止の数学的仕組みなど、**「メカニズム」** に焦点を当てて解説しています。

詳細な解説は以下のドキュメントに分けて記載しています。

## 📚 ドキュメント一覧

### [第1章: JWTの構造とデコード](docs/01_jwt_structure.md)
*   アクセストークン (JWT) の3つのパーツ（ヘッダー、ペイロード、署名）
*   Base64エンコード・デコードの仕組み
*   トークンの中身（クレーム）の詳細解説
*   **ツール**: `decode_jwt.py` の使い方

### [第2章: 署名とセキュリティ検証](docs/02_signature_verification.md)
*   署名 (Signature) の役割と仕組み
*   RSA暗号とSHA-256による改ざん防止
*   なぜHTTPSが必要なのか
*   **ツール**: `verify_signature.py` の使い方（改ざん検知の実験）

## 🛠️ ツール一覧

このリポジトリには、学習用のPythonスクリプトが含まれています。

### 1. `decode_jwt.py`
アクセストークンをデコードして中身を表示します。
*   [解説はこちら](docs/01_jwt_structure.md#4-実践ツール-decode_jwtpy)

### 2. `verify_signature.py`
署名の作成・検証・改ざん検知をシミュレーションします。
*   [解説はこちら](docs/02_signature_verification.md#4-実践ツール-verify_signaturepy)

## 🚀 環境セットアップ

Pythonのパッケージ管理には `uv` を使用しています。

```bash
# 初期化と依存関係のインストール
uv sync
```
