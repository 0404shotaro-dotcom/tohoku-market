import streamlit as st
from database import get_my_items

def show_mypage():
    user = st.session_state.user
    st.title("👤 マイページ")

    st.markdown(f"""
    | 項目 | 内容 |
    |------|------|
    | 氏名 | {user['name']} |
    | メール | {user['email']} |
    | 登録日 | {user['created_at'][:10]} |
    """)

    st.divider()
    st.subheader("📦 出品中の商品")

    items = get_my_items(user["id"])
    if not items:
        st.info("出品中の商品はありません。")
        if st.button("出品する"):
            st.session_state.page = "post"
            st.rerun()
        return

    for item in items:
        status_label = "🟢 出品中" if item["status"] == "available" else "🔴 売却済"
        c1, c2 = st.columns([4, 1])
        with c1:
            st.markdown(f"**{item['title']}**　`{item['category']}`　{status_label}")
            st.caption(f"出品日：{item['created_at'][:10]}　📍 {item.get('meetup_location','未定')}")
        with c2:
            st.markdown(f"**¥{item['price']:,}**")
        st.divider()
