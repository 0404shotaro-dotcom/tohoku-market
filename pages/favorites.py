import streamlit as st
from database import get_favorites

def show_favorites():
    st.title("❤️ お気に入り")
    items = get_favorites(st.session_state.user["id"])

    if not items:
        st.info("お気に入りに追加した商品がありません。")
        return

    for item in items:
        c1, c2 = st.columns([4, 1])
        with c1:
            st.markdown(f"**{item['title']}**　`{item['category']}`")
            st.caption(f"📍 {item.get('meetup_location','未定')}　👤 {item['seller_name']}")
        with c2:
            st.markdown(f"**¥{item['price']:,}**")
            if st.button("詳細", key=f"fav_detail_{item['id']}"):
                st.session_state.selected_item_id = item['id']
                st.session_state.page = "item_detail"
                st.rerun()
        st.divider()
