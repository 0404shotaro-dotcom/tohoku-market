import streamlit as st
from database import post_item
import os
from PIL import Image
import uuid

CATEGORIES = ["教科書", "家具・家電", "衣類・スポーツ", "自転車", "その他"]
LOCATIONS = [
    "川内キャンパス（中央図書館前）",
    "青葉山キャンパス（工学部正門）",
    "星陵キャンパス（医学部前）",
    "片平キャンパス（正門）",
    "その他（チャットで相談）",
]

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_image(uploaded_file) -> str:
    ext = uploaded_file.name.split(".")[-1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    img = Image.open(uploaded_file)
    img.thumbnail((800, 800))
    img.save(filepath)
    return filepath

def show_post():
    st.title("📦 商品を出品する")

    with st.form("post_form"):
        title = st.text_input("商品名 *", placeholder="例：材料力学（第3版）、IKEA デスク")
        category = st.selectbox("カテゴリ *", CATEGORIES)
        price = st.number_input("価格（円） *", min_value=0, max_value=100000, step=100, value=500)
        description = st.text_area("商品説明", placeholder="状態・使用期間・付属品など", height=120)
        meetup_location = st.selectbox("受け渡し希望場所 *", LOCATIONS)

        uploaded_file = st.file_uploader(
            "📷 商品写真（任意）",
            type=["jpg", "jpeg", "png"],
            help="JPG・PNG形式、最大サイズは自動調整されます"
        )

        if uploaded_file:
            st.image(uploaded_file, caption="プレビュー", width=300)

        submitted = st.form_submit_button("出品する", use_container_width=True)

        if submitted:
            if not title:
                st.error("商品名を入力してください。")
            else:
                image_path = None
                if uploaded_file:
                    try:
                        image_path = save_image(uploaded_file)
                    except Exception as e:
                        st.warning(f"写真の保存に失敗しました（{e}）。写真なしで出品します。")

                post_item(
                    seller_id=st.session_state.user["id"],
                    title=title,
                    description=description,
                    price=price,
                    category=category,
                    meetup_location=meetup_location,
                    image_path=image_path
                )
                st.success("✅ 出品しました！ホームに反映されます。")
                st.balloons()
