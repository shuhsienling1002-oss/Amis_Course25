import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心相容性修復 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音生成暫時無法使用)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 25: O Faloco'", page_icon="❤️", layout="centered")

# --- CSS 美化 (情感與暖心色調) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #F8BBD0 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #C2185B;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #880E4F; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #FCE4EC;
        border-left: 5px solid #F48FB1;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #F8BBD0; color: #880E4F; border: 2px solid #C2185B; padding: 12px;
    }
    .stButton>button:hover { background-color: #F48FB1; border-color: #AD1457; }
    .stProgress > div > div > div > div { background-color: #C2185B; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 25: 14個單字 - User Fix) ---
vocab_data = [
    {"amis": "Matawa", "chi": "笑", "icon": "😄", "source": "Row 5"},
    {"amis": "Tangic", "chi": "哭 (詞根)", "icon": "😭", "source": "User Fix"}, # 修正
    {"amis": "Maolah", "chi": "喜歡 / 愛", "icon": "❤️", "source": "Row 18"},
    {"amis": "Mafana'", "chi": "知道 / 認識 / 會", "icon": "💡", "source": "Row 6"},
    {"amis": "Tengil", "chi": "聽 (詞根)", "icon": "👂", "source": "User Fix"}, # 修正
    {"amis": "Soni", "chi": "聲音", "icon": "🔊", "source": "Row 238"},
    {"amis": "Mafoti'", "chi": "睡覺", "icon": "😴", "source": "Row 4"},
    {"amis": "Mipaso'elin", "chi": "相信", "icon": "🙏", "source": "User Fix"}, # 修正
    {"amis": "Mapapadang", "chi": "互相幫忙", "icon": "🤝", "source": "Row 384"},
    {"amis": "Kapah", "chi": "青年 / 年輕人", "icon": "🧑", "source": "Row 4"},
    {"amis": "Widang", "chi": "朋友", "icon": "👯", "source": "Row 508"},
    {"amis": "Tatiih", "chi": "壞的 / 糟糕的", "icon": "👎", "source": "Row 473"},
    {"amis": "Ma^emin", "chi": "全部 / 所有的", "icon": "💯", "source": "Row 508"},
    {"amis": "Matengil", "chi": "聽到 (被動)", "icon": "🎧", "source": "Row 238"},
]

# --- 句子庫 (7句: 嚴格源自 CSV 並移除連字號) ---
sentences = [
    {"amis": "Matawa ci Panay takowanan.", "chi": "Panay笑我。", "icon": "😄", "source": "Row 5"},
    {"amis": "Minokay kako 'i, matengil no mako ko soni no tangic.", "chi": "當我回家的時候，哭聲被我聽見。", "icon": "😭", "source": "Row 238"},
    {"amis": "Mipaso'elin ko widang no mako takowanan a ma^emin.", "chi": "我的朋友全部都相信我。", "icon": "🙏", "source": "Row 508 (Adapted to Mipaso'elin)"},
    {"amis": "Maolah koya a wawa ciiraan.", "chi": "那個小孩喜歡他。", "icon": "❤️", "source": "Row 18"},
    {"amis": "Mafana' ci Kacaw tisowanan.", "chi": "Kacaw認識你。", "icon": "💡", "source": "Row 6"},
    {"amis": "Mafoti' koni a kapah.", "chi": "這位青年在睡覺。", "icon": "😴", "source": "Row 4"},
    {"amis": "Mapapadang kita.", "chi": "大家互相幫忙。", "icon": "🤝", "source": "Row 384"},
]

# --- 3. 隨機題庫 (Synced) ---
raw_quiz_pool = [
    {
        "q": "Matawa ci Panay takowanan.",
        "audio": "Matawa ci Panay takowanan",
        "options": ["Panay笑我", "Panay看我", "Panay罵我"],
        "ans": "Panay笑我",
        "hint": "Matawa (笑) (Row 5)"
    },
    {
        "q": "Minokay kako 'i, matengil no mako...",
        "audio": "Minokay kako 'i, matengil no mako",
        "options": ["被我聽見", "被我看見", "被我聞到"],
        "ans": "被我聽見",
        "hint": "Matengil (被聽見) (Row 238)"
    },
    {
        "q": "單字測驗：Tangic",
        "audio": "Tangic",
        "options": ["哭/哭聲", "笑聲", "歌聲"],
        "ans": "哭/哭聲",
        "hint": "Row 238: ...soni no tangic (哭的聲音)"
    },
    {
        "q": "單字測驗：Mipaso'elin",
        "audio": "Mipaso'elin",
        "options": ["相信", "懷疑", "知道"],
        "ans": "相信",
        "hint": "User Fix: Mipaso'elin"
    },
    {
        "q": "Maolah koya a wawa ciiraan.",
        "audio": "Maolah koya a wawa ciiraan",
        "options": ["那個小孩喜歡他", "那個小孩討厭他", "那個小孩認識他"],
        "ans": "那個小孩喜歡他",
        "hint": "Maolah (喜歡/愛) (Row 18)"
    },
    {
        "q": "單字測驗：Mafoti'",
        "audio": "Mafoti'",
        "options": ["睡覺", "起床", "吃飯"],
        "ans": "睡覺",
        "hint": "Row 4: 青年在 Mafoti'"
    },
    {
        "q": "單字測驗：Tengil",
        "audio": "Tengil",
        "options": ["聽 (詞根)", "看 (詞根)", "說 (詞根)"],
        "ans": "聽 (詞根)",
        "hint": "耳朵的功能"
    },
    {
        "q": "單字測驗：Kapah",
        "audio": "Kapah",
        "options": ["青年/年輕人", "老人", "小孩"],
        "ans": "青年/年輕人",
        "hint": "Row 4: Mafoti' koni a kapah"
    }
]

# --- 4. 狀態初始化 (洗牌邏輯) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 抽題與洗牌
    selected_questions = random.sample(raw_quiz_pool, 3)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #880E4F;'>Unit 25: O Faloco'</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>情緒與感受 (User Corrected)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字 (從句子提取)")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型 (Data-Driven)")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #880E4F;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 ===
with tab2:
    st.markdown("### 🎲 隨機評量")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        st.progress((st.session_state.current_q_idx) / 3)
        st.markdown(f"**Question {st.session_state.current_q_idx + 1} / 3**")
        
        st.markdown(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        # 使用洗牌後的選項
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['shuffled_options'], key=unique_key)
        
        if st.button("送出答案", key=f"btn_submit_{st.session_state.current_q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("🎉 答對了！")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q_idx += 1
                safe_rerun()
            else:
                st.error(f"不對喔！提示：{q_data['hint']}")
                
    else:
        st.progress(1.0)
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #F8BBD0; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #880E4F;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經學會表達情緒了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再來一局 (重新抽題)", key="btn_restart"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_id = str(random.randint(1000, 9999))
            
            new_questions = random.sample(raw_quiz_pool, 3)
            final_qs = []
            for q in new_questions:
                q_copy = q.copy()
                shuffled_opts = random.sample(q['options'], len(q['options']))
                q_copy['shuffled_options'] = shuffled_opts
                final_qs.append(q_copy)
            
            st.session_state.quiz_questions = final_qs
            safe_rerun()
