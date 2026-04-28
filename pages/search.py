import streamlit as st
from database import get_items

CATEGORIES = ["すべて", "教科書", "家具・家電", "衣類・スポーツ", "自転車", "その他"]

def show_search():
    st.title("🔍 商品を探す")

    col1, col2 = st.columns([3, 1])
    with col1:
        keyword = st.text_input("キーワード検索", placeholder="例：材料力学、冷蔵庫、自転車...")
    with col2:
        category = st.selectbox("カテゴリ", CATEGORIES)

    items = get_items(
        category=category if category != "すべて" else None,
        keyword=keyword if keyword else None
    )

    st.markdown(f"**{len(items)} 件** 見つかりました")
    st.divider()

    if not items:
        st.info("該当する商品が見つかりませんでした。")
        return

    for item in items:
        with st.container():
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"**{item['title']}**　`{item['category']}`")
                st.caption(f"{item.get('description','')[:80]}")
                st.caption(f"📍 {item.get('meetup_location','未定')}　👤 {item['seller_name']}")
            with c2:
                st.markdown(f"**¥{item['price']:,}**")
                if st.button("詳細", key=f"s_detail_{item['id']}"):
                    st.session_state.selected_item_id = item['id']
                    st.session_state.page = "item_detail"
                    st.rerun()
            st.divider()
