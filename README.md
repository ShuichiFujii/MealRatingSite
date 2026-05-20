# Meal Ratings Site

![Python](https://img.shields.io/badge/Python-3.12.7-blue)
![Django](https://img.shields.io/badge/Django-6.0.4-green)
![CI](https://github.com/ShuichiFujii/MealRatingSite/actions/workflows/django-tests.yml/badge.svg)
![Status](https://img.shields.io/badge/status-maintained-blue)

## Overview

Django を用いて作成した 食事評価サイト (Meal Rating Site) です。

ユーザーは料理に対して評価（★1〜5）とコメントを投稿でき、
他のユーザーの評価を閲覧することができます。

このプロジェクトでは以下の点を重点的に実装しました。

- Django による Web アプリケーション開発
- モデル設計とリレーション管理
- フォームバリデーション
- View のテスト
- GitHub Actions を用いた CI（自動テスト）

## Screenshot

### Landing Page
<img src="docs/images/landing-page.png" alt="Landing Page" width="400">

### Category List Page
<img src="docs/images/category-list-page.png" alt="Category List Page" width="400">

### Meal Detail Page
<img src="docs/images/meal-detail-page.png" alt="Meal Detail Page" width="400">

## Features

主な機能

- 食事の登録
- 食事一覧表示
- 食事詳細ページ
- 食事の評価投稿（★1〜5）
- コメント投稿
- 評価平均値の自動更新
- ページネーション
- カテゴリ別表示
    - 朝食
    - 昼食
    - 夕食
    - 新着
    - 高評価
- 並び替え
    - 評価順
    - 新着順
    - 国名のアルファベット順

## Tech Stack

使用技術
- Python 3.12.7
- Django 6.0.4
- Pillow 12.2.0 (画像アップロード用)
- SQLite (開発用データベース)

CI
- GitHub Actions (自動テスト)

## Setup

### Environment Variables

このプロジェクトでは環境変数を `.env` ファイルで管理します。

まず `.env.example` をコピーして `.env` を作成してください。

macOS / Linux:
```bash
cp .env.example .env
```

Windows:
```bash
copy .env.example .env
```

SECRET_KEY の生成には補助スクリプトを利用できます。

```bash
python scripts/generate_secret_key.py
```

生成した値を `.env` の `DJANGO_SECRET_KEY` に設定してください。

CI (GitHub Actions) では、テスト実行専用の固定 SECRET_KEY を環境変数として直接設定しています。
これは本番用途ではなく、再現可能なテスト環境を簡単に構築するためです。


### Manual Setup

ローカル環境での実行方法

1. リポジトリをクローン
    ```bash
    git clone https://github.com/ShuichiFujii/MealRatingSite.git
    cd MealRatingSite
    ```

2. 仮想環境作成
   
   このプロジェクトは、Python 3.12.7 を前提としています。

   環境によって `python` が別バージョンを指す場合があるため、
   必要に応じて `python3.12` を使用してください。
   
    ```bash
    python -m venv .venv
    ```

3. 仮想環境起動
    - Windows
        ```bash
        .venv\Scripts\activate
        ```
    - macOS/Linux
        ```bash
        source .venv/bin/activate
        ```

4. 依存関係インストール
    ```bash
    pip install -r requirements.txt
    ```

5. データベースマイグレーション
    ```bash
    python manage.py migrate
    ```

6. サンプルデータのロード（Optional）

   fixtures を用意しているため、サンプルデータをロードできます。
   ```bash
   python manage.py loaddata meals
   ```

7. 開発サーバー起動
    ```bash
    python manage.py runserver
    ```

---

### Helper Script

Windows 環境では、以下の補助スクリプトを利用できます。

| Command | Description |
|---|---|
| `run setup` | 仮想環境作成、依存関係インストール、マイグレーションを実行 |
| `run server` | 開発サーバーを起動 |
| `run test` | Django のテストを実行 |
| `run migrate` | マイグレーションを作成・適用 |

## Usage

サーバーを起動後、ブラウザで `http://localhost:8000/` にアクセスしてください。

できること
- 食事の一覧を見る
- 食事の詳細を見る
- 食事を登録する
- 評価とコメントを投稿する
- カテゴリ別に食事を表示する
- 評価順・新着順・国名のアルファベット順

## Tests

テストは Django の `TestCase` を用いて実装しています。

テストの実行方法は以下の通りです。

```bash
python manage.py test
```

テスト対象
- models.py
- views.py
- forms.py

## CI

GitHub Actions を用いて、プッシュやプルリクエスト時に自動でテストが実行されるように設定しています。

## Design

### Meal と MealRating の分離

食事 (`Meal`) とユーザー評価 (`MealRating`) を別モデルとして設計しました。

`MealRating` は `Meal` に対する `ForeignKey` を持ち、
1つの食事に複数の評価を紐づけることができます。

また、個々の評価は `MealRating` に保存し、
平均評価 (`average_rating`) と評価件数 (`number_of_votes`) は 
`Meal` 側で集計結果として保持しています。

これにより、食事一覧では集計済みの評価を表示しやすく、
詳細ページでは個別のコメントも扱いやすい構造にしています。

### 評価の集計

評価が投稿された後、`update_rating_stats()` を呼び出し  
平均評価 (`average_rating`) と投票数 (`number_of_votes`) を更新しています。

## Future Improvements

今後追加予定の機能
- ユーザー認証機能
- 評価編集 / 削除
- 人気ランキング
- API化

## Author

### GitHub

[Shuichi Fujii](https://github.com/ShuichiFujii)

### Qiita

学習内容や開発中に得た知見を技術記事として投稿しています。

[Qiita - embermaverick05](https://qiita.com/embermaverick05)
