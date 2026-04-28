# 🎓 Tohoku Market

東北大学専用フリーマーケットWebアプリ（Streamlit + SQLite）

## セットアップ手順

### 1. Pythonのインストール確認
```bash
python --version  # 3.8以上であること
```

### 2. Streamlitのインストール
```bash
pip install streamlit
```

### 3. アプリの起動
```bash
cd tohoku_market
streamlit run app.py
```

ブラウザが自動で開き、`http://localhost:8501` でアプリが表示されます。

## ファイル構成

```
tohoku_market/
├── app.py              # メインアプリ・ルーティング・認証
├── database.py         # SQLite操作（登録・ログイン・商品・チャット）
├── requirements.txt    # 必要パッケージ
└── pages/
    ├── home.py         # ホーム画面（カテゴリ・新着）
    ├── search.py       # 商品検索
    ├── post.py         # 出品フォーム
    ├── item_detail.py  # 商品詳細・チャット
    ├── favorites.py    # お気に入り一覧
    └── mypage.py       # マイページ・出品履歴
```

## 機能一覧

- ✅ 東北大学メール認証（@tohoku.ac.jp のみ登録可）
- ✅ 商品出品（カテゴリ・価格・説明・受け渡し場所）
- ✅ 商品検索（キーワード・カテゴリ）
- ✅ チャット機能（購入相談・日時調整）
- ✅ お気に入り保存
- ✅ マイページ（出品履歴）

## 今後の追加予定

- 📷 商品写真のアップロード
- 🔔 メッセージ通知
- ⭐ レビュー機能
- 📚 教科書専用検索（授業名・ISBN）
