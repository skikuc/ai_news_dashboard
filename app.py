import streamlit as st
import feedparser
import datetime
import urllib.parse

# ページ設定
st.set_page_config(
    page_title="坂本慎太郎・記事",
    page_icon="🎸",
    layout="wide"
)

# サイドバー設定（検索機能は今回は非表示）
# st.sidebar.header("検索設定")
search_query = "坂本慎太郎"

# CSSによるカードデザインの定義
st.markdown("""
<style>
    /* 全体のフォントと背景設定 */
    .stApp {
        background-color: #f8f9fa;
        color: #333333;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    
    /* カードデザインの更新 */
    .news-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border: 1px solid #eaeaea;
    }
    .news-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }
    
    /* タイトルデザイン */
    .news-title {
        color: #1a1a1a;
        font-size: 1.3em;
        font-weight: 700;
        margin-bottom: 12px;
        text-decoration: none;
        display: block;
        line-height: 1.4;
    }
    .news-title:hover {
        color: #0066cc;
        text-decoration: underline;
    }
    
    /* メタ情報（日付など） */
    .news-meta {
        color: #888;
        font-size: 0.85em;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
    }
    
    /* 記事要約 */
    .news-summary {
        color: #555;
        font-size: 0.95em;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    
    /* ボタンデザイン */
    .news-link-btn {
        display: inline-block;
        background-color: #0066cc;
        color: white !important;
        padding: 8px 16px;
        text-decoration: none;
        border-radius: 6px;
        font-size: 0.9em;
        font-weight: 500;
        transition: background-color 0.2s;
    }
    .news-link-btn:hover {
        background-color: #0052a3;
    }

    /* ダークモードの強制無効化（ライトモード固定のための上書き） 
       Streamlitの仕様上、st.set_page_configだけでは完全に制御できない部分を補完
    */
    @media (prefers-color-scheme: dark) {
        .news-card {
            background-color: #ffffff;
        }
        .news-title {
            color: #1a1a1a;
        }
        .news-meta {
            color: #888;
        }
        .news-summary {
            color: #555;
        }
    }
</style>
""", unsafe_allow_html=True)

# メインコンテンツ
st.markdown("<h1 style='font-size: 2.5rem;'>🎸 坂本慎太郎・記事</h1>", unsafe_allow_html=True)
# st.subheader(f"「{search_query}」の最新ニュース") # タイトルで十分なためサブヘッダーはシンプルに
st.markdown("---")

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
