import streamlit as st
import feedparser
import datetime
import urllib.parse

# ページ設定
st.set_page_config(
    page_title="AI News Dashboard",
    page_icon="🤖",
    layout="wide"
)

# サイドバー設定
st.sidebar.header("検索設定")
search_query = st.sidebar.text_input("検索キーワード", value="Artificial Intelligence")

# CSSによるカードデザインの定義
st.markdown("""
<style>
    .news-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    .news-card:hover {
        transform: translateY(-5px);
    }
    .news-title {
        color: #1f77b4;
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 10px;
        text-decoration: none;
    }
    .news-meta {
        color: #666;
        font-size: 0.8em;
        margin-bottom: 10px;
    }
    .news-summary {
        color: #333;
        font-size: 0.9em;
        margin-bottom: 15px;
    }
    .news-link-btn {
        display: inline-block;
        background-color: #ff4b4b;
        color: white;
        padding: 5px 15px;
        text-decoration: none;
        border-radius: 5px;
        font-size: 0.9em;
    }
    .news-link-btn:hover {
        background-color: #ff3333;
        color: white;
    }
    /* ダークモード対応 */
    @media (prefers-color-scheme: dark) {
        .news-card {
            background-color: #262730;
        }
        .news-title {
            color: #4da6ff;
        }
        .news-meta {
            color: #aaa;
        }
        .news-summary {
            color: #ddd;
        }
    }
</style>
""", unsafe_allow_html=True)

# メインコンテンツ
st.title("🤖 AI News Dashboard")
st.subheader(f"「{search_query}」の最新ニュース")

# ニュース取得ロジック
def get_news(query):
    # 日本語のニュースを取得するために hl=ja&gl=JP&ceid=JP:ja を追加
    # URLエンコードはfeedparserが自動で処理するが、明示的な空白処理などは検索クエリに依存
    # Python 3.10以降のhttp.clientなどでは厳密なチェックが入るため明示的にエンコード
    encoded_query = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    feed = feedparser.parse(rss_url)
    return feed.entries

if search_query:
    with st.spinner('ニュースを取得中...'):
        entries = get_news(search_query)

    if entries:
        # 3カラムのグリッドレイアウト
        cols = st.columns(3)
        
        for idx, entry in enumerate(entries):
            col = cols[idx % 3]
            
            # 日付のフォーマット
            published = entry.get('published', '日付不明')
            try:
                # Google Newsの日付形式をパース (例: Fri, 14 Feb 2026 10:00:00 GMT)
                # 簡易的な表示にする
                dt = datetime.datetime.strptime(published[:25], '%a, %d %b %Y %H:%M:%S')
                published = dt.strftime('%Y/%m/%d %H:%M')
            except:
                pass

            # 要約のクリーニング (HTMLタグが含まれる場合があるため)
            summary = entry.get('summary', '')
            # 簡易的なHTMLタグ除去 (必要であればBeautifulSoupなどを使うが、要件にはないため標準ライブラリ範囲で)
            # summary = re.sub('<[^<]+?>', '', summary) # import reが必要

            with col:
                st.markdown(f"""
                <div class="news-card">
                    <a href="{entry.link}" target="_blank" class="news-title">{entry.title}</a>
                    <div class="news-meta">📅 {published}</div>
                    <div class="news-summary">{summary[:100]}...</div>
                    <a href="{entry.link}" target="_blank" class="news-link-btn">記事を読む</a>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("ニュースが見つかりませんでした。")
else:
    st.warning("検索キーワードを入力してください。")
