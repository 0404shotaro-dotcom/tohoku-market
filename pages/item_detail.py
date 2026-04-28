import streamlit as st
import os
from database import get_item_by_id, send_message, get_messages, toggle_favorite

def show_item_detail():
    item_id = st.session_state.get("selected_item_id")
    if not item_id:
        st.error("商品が見つかりません。")
        return

    item = get_item_by_id(item_id)
    if not item:
        st.error("商品が見つかりません。")
        return

    if st.button("← 戻る"):
        st.session_state.page = "home"
        st.rerun()

    st.title(item["title"])

    col1, col2 = st.columns([2, 1])
    with col1:
        # 写真表示
        if item.get("image_path") and os.path.exists(item["image_path"]):
            st.image(item["image_path"], use_container_width=True)
        else:
            st.markdown("""
            <div style="background:#f0f4fa; border-radius:12px; height:200px;
                        display:flex; align-items:center; justify-content:center; color:#aaa; font-size:2rem;">
                📷
            </div>
            """, unsafe_allow_html=True)
        st.markdown(f"**カテゴリ：** `{item['category']}`")
        st.markdown(f"**説明：** {item.get('description', '説明なし')}")
        st.markdown(f"**受け渡し場所：** 📍 {item.get('meetup_location', '未定')}")
        st.markdown(f"**出品者：** 👤 {item['seller_name']}")
    with col2:
        st.markdown(f"### ¥{item['price']:,}")
        # お気に入りボタン
        if st.button("❤️ お気に入り登録/解除", use_container_width=True):
            added = toggle_favorite(st.session_state.user["id"], item_id)
            st.success("お気に入りに追加しました！" if added else "お気に入りから削除しました。")
            st.rerun()

    st.divider()

    # 自分の出品は購入不可
    user_id = st.session_state.user["id"]
    if item["seller_id"] == user_id:
        st.info("これはあなたの出品商品です。")
        return

    # チャット
    st.subheader("💬 出品者にメッセージ")
    messages = get_messages(item_id, user_id)

    chat_container = st.container()
    with chat_container:
        if not messages:
            st.caption("まだメッセージはありません。気軽に質問してみましょう！")
        for msg in messages:
            is_mine = msg["sender_id"] == user_id
            alignment = "right" if is_mine else "left"
            bg = "#d0e8ff" if is_mine else "#f0f0f0"
            name = "あなた" if is_mine else msg["sender_name"]
            st.markdown(f"""
            <div style="text-align:{alignment}; margin:4px 0;">
                <span style="font-size:0.75rem; color:#888;">{name}</span><br>
                <span style="background:{bg}; padding:6px 12px; border-radius:16px; display:inline-block; max-width:70%;">
                    {msg['message']}
                </span>
            </div>
            """, unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        msg_text = st.text_input("メッセージを入力", placeholder="受け渡しの日時・場所の相談など")
        sent = st.form_submit_button("送信", use_container_width=True)
        if sent and msg_text:
            send_message(
                item_id=item_id,
                sender_id=user_id,
                receiver_id=item["seller_id"],
                message=msg_text
            )
            st.rerun()
