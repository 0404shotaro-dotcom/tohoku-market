import streamlit as st
import os
from database import get_items

CATEGORIES = ["すべて", "教科書", "家具・家電", "衣類・スポーツ", "自転車", "その他"]

def item_card(item):
    with st.container():
        if item.get("image_path") and os.path.exists(item["image_path"]):
            st.image(item["image_path"], use_container_width=True)
        st.markdown(f"""
        <div class="item-card">
            <span class="category-badge">{item['category']}</span>
            <h3 style="margin: 0.5rem 0 0.2rem;">{item['title']}</h3>
            <p style="color:#666; font-size:0.9rem; margin:0 0 0.5rem;">{item['description'][:60] + '...' if item['description'] and len(item['description']) > 60 else item.get('description','')}</p>
            <div class="price-tag">¥{item['price']:,}</div>
            <p style="color:#999; font-size:0.8rem; margin:0.3rem 0 0;">出品者：{item['seller_name']} ｜ 受け渡し：{item.get('meetup_location','未定')}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("詳細を見る", key=f"detail_{item['id']}"):
            st.session_state.selected_item_id = item['id']
            st.session_state.page = "item_detail"
            st.rerun()

def show_home():
    st.markdown("""
    <div class="main-header">
        <h1>🎓 Tohoku Market</h1>
        <p>東北大学メンバー限定 ・ 学内手渡し ・ 送料ゼロ</p>
    </div>
    """, unsafe_allow_html=True)

    # カテゴリフィルタ
    st.subheader("カテゴリから探す")
    cols = st.columns(len(CATEGORIES))
    selected_cat = st.session_state.get("home_category", "すべて")
    for i, cat in enumerate(CATEGORIES):
        with cols[i]:
            if st.button(cat, use_container_width=True, key=f"cat_{cat}",
                         type="primary" if selected_cat == cat else "secondary"):
                st.session_state.home_category = cat
                st.rerun()

    st.divider()

    # 新着商品
    st.subheader("📦 新着商品")
    cat_filter = st.session_state.get("home_category", "すべて")
    items = get_items(category=cat_filter if cat_filter != "すべて" else None)

    if not items:
        st.info("まだ商品がありません。最初の出品者になりましょう！")
        if st.button("出品する"):
            st.session_state.page = "post"
            st.rerun()
    else:
        cols = st.columns(2)
        for i, item in enumerate(items):
            with cols[i % 2]:
                item_card(item)
