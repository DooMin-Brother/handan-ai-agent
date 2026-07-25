import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(
    page_title="한단제어기술 AI 기술지원",
    page_icon="🤖",
    layout="wide"
)

# 2. Sidebar Configuration
st.sidebar.title("🏢 한단제어기술")
st.sidebar.caption("FA 자동화, PLC 및 모션 제어 전문 기업")
st.sidebar.markdown("[👉 공식 홈페이지 방문](http://handancity.com)")

st.sidebar.markdown("---")
st.sidebar.subheader("취급품목")
st.sidebar.markdown("""
* **PLC**
* **모션콘트롤러**
* **SERVO**
* **감속기**
* **INVERTER**
* **직교좌표 로봇**
* **ROBOT**
* **파워롤러**
* **DD MOTOR**
""")

st.sidebar.subheader("주요 공급 브랜드")
st.sidebar.markdown("""
* **한국미쓰비시전기 대리점**
* **보쉬렉스로스 대리점**
* **이노밴스 대리점**
* **스토버 대리점**
* **SPG 대리점**
* **휴림로봇 대리점**
* **맘바롤 대리점**
* **신포니아 대리점**
""")

st.sidebar.markdown("---")
st.sidebar.subheader("📝 오늘 질의 응답 레포트 작성")
st.sidebar.caption("오늘의 대화 내용을 기반으로 기술지원 리포트를 작성해 드립니다.")
if st.sidebar.button("📄 레포트 작성 요청"):
    st.sidebar.info("레포트 생성 기능이 곧 준비될 예정입니다.")

st.sidebar.markdown("---")
st.sidebar.subheader("📞 기술 지원 & 고객센터")
st.sidebar.markdown("[💬 카카오톡 1:1 실시간 상담](http://pf.kakao.com)")
st.sidebar.caption("전화: 031-4798-4970")
st.sidebar.caption("이메일: handancity@handancity.co.kr")

st.sidebar.markdown("---")
st.sidebar.caption("🔒 업로드한 자료와 대화 내용은 문제 해결을 위해서만 사용됩니다.")

# 3. Main Interface Header
st.title("🤖 한단제어기술 AI 기술지원 & 매뉴얼 비서")
st.caption("업로드된 기술 매뉴얼 및 현장 자료를 바탕으로 정확하고 빠르게 답변해 드립니다.")

st.subheader("AI 답변")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# File Upload Section
uploaded_file = st.file_uploader(
    "자료 첨부", 
    type=["pdf", "txt", "png", "jpg", "mp4", "mov"],
    help="200MB per file • PDF, TXT, PNG, JPG, MP4, MOV"
)

# User Input Section
col1, col2 = st.columns([4, 1])

with col1:
    user_prompt = st.text_input("AI에게 기술 질문을 입력하세요...", key="user_input")

with col2:
    voice_btn = st.button("🎙️ 음성 질의")

# Gemini API Integration & Response Generation
if user_prompt:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    # Configure API Key & Model
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # 최신 표준 모델명으로 지정
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        with st.spinner("AI가 기술 자료를 분석 중입니다..."):
            response = model.generate_content(user_prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except KeyError:
        st.error("API 키 설정 오류: Streamlit Secrets에 GEMINI_API_KEY가 설정되지 않았습니다.")
    except Exception as e:
        st.error(f"답변 생성 오류: {e}")

# Display response box (대화 내역 표시 위치 조정)
with st.container(border=True):
    if not st.session_state.messages:
        st.info("💬 AI가 답변을 여기에 표시합니다. 질문을 입력하거나 음성으로 말씀해 주세요.")
    else:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

st.markdown("""
<small style='color: gray;'>
• 음성 질의 응답 시 음성 버튼을 누르고 질의 응답을 하시고<br>
• 문자 질의 응답 시 문자입력 창에 입력하여 질의 응답을 하십시오<br>
• 자료는 문자, 파일, 사진, 스캔화면, 동영상 등을 드래그하여 올려 주십시오.
</small>
""", unsafe_allow_html=True)
