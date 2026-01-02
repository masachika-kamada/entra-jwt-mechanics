# Entra JWT Mechanics

このリポジトリは、Microsoft Entra ID (旧 Azure AD) のアクセストークンや JWT (JSON Web Token) の仕組み、およびリフレッシュトークンによる更新フローについて学習した内容と、検証用コードをまとめたものです。

アクセストークンの内部構造、RSA署名による改ざん防止の仕組み、そしてOAuth 2.0のリフレッシュトークンフローなど、**「メカニズム」** に焦点を当てて解説しています。

## 📂 ディレクトリ構成

学習しやすいように、章ごとにディレクトリを分けています。

```text
entra-learn/
├── 01_jwt_structure/    # 第1章: JWTの構造とデコード
├── 02_signature/        # 第2章: 署名とセキュリティ検証
├── 03_refresh_token/    # 第3章: リフレッシュトークンによる更新
├── .env.example         # 環境変数のテンプレート
├── pyproject.toml       # 依存関係の定義
└── uv.lock              # バージョン固定ファイル
```

## 📚 学習コンテンツ

各ディレクトリにある `README.md` に詳細な解説があります。

### [第1章: JWTの構造とデコード](01_jwt_structure/README.md)
*   アクセストークン (JWT) の3つのパーツ（ヘッダー、ペイロード、署名）
*   Base64エンコード・デコードの仕組み
*   **実践**: `decode_jwt.py` を使ってトークンの中身を覗いてみる

### [第2章: 署名とセキュリティ検証](02_signature/README.md)
*   署名 (Signature) の役割と仕組み
*   RSA暗号とSHA-256による改ざん防止
*   **実践**: `verify_signature.py` で署名の作成と改ざん検知をシミュレーション

### [第3章: リフレッシュトークンによる更新](03_refresh_token/README.md)
*   アクセストークンの有効期限と更新フロー
*   SPA (Single Page Application) におけるセキュリティ制約 (Originヘッダー)
*   トークンローテーション（更新ごとのトークン変更）
*   **実践**: `refresh_token_client.py` で実際にトークンを更新してみる

## 🚀 環境セットアップ

このプロジェクトでは、Pythonのパッケージ管理に **`uv`** を使用しています。

### 1. 依存関係のインストール

```bash
# リポジトリのクローン（まだの場合）
git clone <repository-url>
cd entra-learn

# 依存パッケージのインストール
uv sync
```

### 2. 各章の学習

各ディレクトリに移動して、READMEを読みながら学習を進めてください。

*   **[01_jwt_structure/](01_jwt_structure/README.md)**: JWTの構造理解
*   **[02_signature/](02_signature/README.md)**: 署名の検証実験
*   **[03_refresh_token/](03_refresh_token/README.md)**: トークン更新の実践（※設定が必要です）

### 3. スクリプトの実行

```bash
# 例: 第3章のスクリプトを実行する場合
cd 03_refresh_token
uv run refresh_token_client.py
```
