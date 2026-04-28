import streamlit as st
from database import init_db, login_user, register_user

# DB初期化
init_db()

# ページ設定
st.set_page_config(
    page_title="Tohoku Market",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Noto Sans JP', sans-serif;
    }
    .main-header {
        background: linear-gradient(135deg, #1a3a6e 0%, #2B5EA7 60%, #4a90d9 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .main-header h1 { font-size: 2.5rem; margin: 0; letter-spacing: 2px; }
    .main-header p  { margin: 0.5rem 0 0; opacity: 0.85; font-size: 1rem; }

    .stButton > button {
        background: linear-gradient(135deg, #2B5EA7, #4a90d9);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 700;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.85; }

    .item-card {
        background: white;
        border: 1px solid #e8edf5;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(43,94,167,0.07);
        transition: box-shadow 0.2s;
    }
    .item-card:hover { box-shadow: 0 4px 16px rgba(43,94,167,0.15); }
    .price-tag {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2B5EA7;
    }
    .category-badge {
        background: #e8f0fa;
        color: #2B5EA7;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .sidebar-logo {
        text-align: center;
        padding: 1rem 0;
        font-size: 1.5rem;
        font-weight: 700;
        color: #2B5EA7;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# セッション初期化
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "home"

# ---- ログイン・登録画面 ----
def show_auth():
    st.markdown("""
    <div class="main-header">
        <h1>🎓 Tohoku Market</h1>
        <p>東北大学専用フリーマーケット</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["ログイン", "新規登録"])

    with tab1:
        with st.form("login_form"):
            email = st.text_input("メールアドレス", placeholder="xxx@tohoku.ac.jp")
            password = st.text_input("パスワード", type="password")
            submitted = st.form_submit_button("ログイン", use_container_width=True)
            if submitted:
                result = login_user(email, password)
                if result["success"]:
                    st.session_state.user = result["user"]
                    st.success("ログイン成功！")
                    st.rerun()
                else:
                    st.error(result["error"])

    with tab2:
        with st.form("register_form"):
            name = st.text_input("氏名")
            email = st.text_input("東北大学メール", placeholder="xxx@tohoku.ac.jp")
            password = st.text_input("パスワード（6文字以上）", type="password")
            submitted = st.form_submit_button("登録する", use_container_width=True)
            if submitted:
                if len(password) < 6:
                    st.error("パスワードは6文字以上にしてください。")
                else:
                    result = register_user(email, password, name)
                    if result["success"]:
                        st.success("登録完了！ログインしてください。")
                    else:
                        st.error(result["error"])

# ---- サイドバー ----
def show_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">🎓 Tohoku Market</div>', unsafe_allow_html=True)
        st.markdown(f"**{st.session_state.user['name']}** さん")
        st.divider()

        pages = {
            "🏠 ホーム": "home",
            "🔍 商品を探す": "search",
            "📦 出品する": "post",
            "❤️ お気に入り": "favorites",
            "👤 マイページ": "mypage",
        }
        for label, key in pages.items():
            if st.button(label, use_container_width=True, key=f"nav_{key}"):
                st.session_state.page = key
                st.rerun()

        st.divider()
        if st.button("🚪 ログアウト", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = "home"
            st.rerun()

# ---- メインルーティング ----
if st.session_state.user is None:
    show_auth()
else:
    show_sidebar()

    page = st.session_state.page

    if page == "home":
        from pages.home import show_home
        show_home()
    elif page == "search":
        from pages.search import show_search
        show_search()
    elif page == "post":
        from pages.post import show_post
        show_post()
    elif page == "favorites":
        from pages.favorites import show_favorites
        show_favorites()
    elif page == "mypage":
        from pages.mypage import show_mypage
        show_mypage()
    elif page == "item_detail":
        from pages.item_detail import show_item_detail
        show_item_detail()
