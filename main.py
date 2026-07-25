import os
import io
import streamlit as st
from google import genai
from google.genai import types
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="한단제어기술 AI 기술지원 & 매뉴얼 비서",
    page_icon="🤖",
    layout="wide"
)

# 2. 커스텀 CSS (기존 디자인 100% 유지)
st.markdown("""
    <style>
    .main-header { font-size: 22px; font-weight: bold; margin-bottom: 4px; color: #111; }
    .sub-header { color: #666; font-size: 13px; margin-bottom: 25px; }
    .section-title { font-size: 14px; font-weight: bold; margin-top: 15px; margin-bottom: 5px; color: #333; }
    .sidebar-text { font-size: 12px; color: #444; line-height: 1.6; }
    .stButton>button { width: 100%; border-radius: 6px; }
    
    .footer-instruction {
        font-size: 12px;
        color: #555;
        line-height: 1.5;
        margin-top: 8px;
        padding-left: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# 🔑 API Key 설정
# ------------------------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "여기에_실제_Gemini_API_키를_입력하세요")

client = None
if GEMINI_API_KEY and GEMINI_API_KEY != "여기에_실제_Gemini_API_키를_입력하세요":
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        st.error(f"API Client 초기화 실패: {e}")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# 1. 좌측 사이드바 영역 (기존 복원)
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style='margin-bottom: 2px;'>
        <span style='font-size: 20px; font-weight: bold; color: #111111;'>🏢 한단제어기술</span>
    </div>
    <div style='font-size: 13px; color: #666666; margin-bottom: 6px;'>
        FA 자동화, PLC 및 모션 제어 전문 기업
    </div>
    <div style='margin-bottom: 10px;'>
        <a href='http://handancity.co.kr' target='_blank' style='text-decoration: none; color: #1a73e8; font-size: 13px; font-weight: bold;'>
            👉 공식 홈페이지 방문
        </a>
    </div>

    <!-- 얇고 상하 여백이 매우 좁은 커스텀 구분선 (여백 8px) -->
    <hr style='margin: 8px 0; border: none; border-top: 1px solid #e0e0e0;'>

    <!-- 취급품목 제목 (상단 여백 4px) -->
    <div style='font-size: 15px; font-weight: bold; margin-top: 4px; margin-bottom: 6px; color: #111111;'>
        취급품목
    </div>

    <!-- 취급품목 내용 -->
    <div style='font-size: 14px; font-weight: bold; line-height: 1.4; color: #111111;'>
        • PLC<br>
        • 모션콘트롤러<br>
        • SERVO<br>
        • 감속기<br>
        • INVERTER<br>
        • 직교좌표 로봇<br>
        • ROBOT<br>
        • 파워롤러<br>
        • DD MOTOR
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>주요 공급 브랜드</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size: 14px; font-weight: bold; line-height: 1.8; color: #111111;'>
    • 한국미쓰비시전기 대리점<br>
    • 보쉬렉스로스 대리점<br>
    • 이노밴스 대리점<br>
    • 스토버 대리점<br>
    • SPG 대리점<br>
    • 휴림로봇 대리점<br>
    • 맘바롤 대리점<br>
    • 신포니아 대리점
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("<div class='section-title'>📄 오늘 질의 응답 레포트 작성</div>", unsafe_allow_html=True)
    st.caption("오늘의 대화 내용을 기반으로 기술지원 리포트를 작성해 드립니다.")
    if st.button("📝 레포트 작성 요청"):
        if st.session_state.messages:
            st.toast("오늘의 상담 대화를 기반으로 기술지원 리포트를 생성합니다.", icon="ℹ️")
        else:
            st.warning("작성된 대화 내역이 없습니다.")

    st.divider()

    st.markdown("<div class='section-title'>📞 기술 지원 & 고객센터</div>", unsafe_allow_html=True)
    st.link_button("💬 카카오톡 1:1 실시간 상담", "https://pf.kakao.com")
    st.markdown("""
    <div class='sidebar-text' style='margin-top: 8px;'>
    <b>전화:</b> 031-4798-4970<br>
    <b>이메일:</b> handancity@handancity.co.kr
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.caption("🛡️ 업로드한 자료와 대화 내용은 문제 해결을 위해서만 사용됩니다.")


# ==========================================
# 2. 메인 화면 영역 (기존 복원)
# ==========================================
st.markdown("<div class='main-header'>🤖 한단제어기술 AI 기술지원 & 매뉴얼 비서</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>업로드된 기술 매뉴얼 및 현장 자료를 바탕으로 정확하고 빠르게 답변해 드립니다.</div>", unsafe_allow_html=True)

st.markdown("### AI 답변")

# 대화 내용 출력 영역 (스크롤 박스)
chat_container = st.container(height=480)

with chat_container:
    if not st.session_state.messages:
        st.info("💬 AI가 답변을 여기에 표시합니다. 질문을 입력하거나 음성으로 말씀해 주세요.")
    else:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                # 답변에 음성이 포함되어 있으면 재생 플레이어 표시
                if "audio" in msg:
                    st.audio(msg["audio"], format="audio/mp3")


# ==========================================
# 3. 하단 통합 입력 바 및 원버튼 마이크
# ==========================================
st.write("")

# 파일 업로드
uploaded_files = st.file_uploader(
    "자료 첨부 (문자, 파일, 사진, 스캔화면, 동영상 등을 드래그하여 올려주십시오)",
    type=["pdf", "txt", "png", "jpg", "jpeg", "mp4", "mov"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

col_input, col_voice = st.columns([0.80, 0.20])

with col_input:
    user_text = st.chat_input("AI에게 기술 질문을 입력하세요...")

with col_voice:
    # 원버튼 음성 녹음 위젯
    audio_data = mic_recorder(
        start_prompt="🎙️ 음성 질의",
        stop_prompt="🛑 녹음 완료",
        key='recorder',
        just_once=True
    )

st.markdown("""
<div class='footer-instruction'>
• <b>음성 질의 응답 시</b> 음성 버튼을 누르고 질의 응답을 하시고<br>
• <b>문자 질의 응답 시</b> 문자입력 창에 입력하여 질의 응답을 하십시오<br>
• <b>자료는</b> 문자, 파일, 사진, 스캔화면, 동영상 등을 드래그인하여 올려 주십시오.
</div>
""", unsafe_allow_html=True)


# ==========================================
# 4. 질문 처리 및 gTTS 음성 생성 로직
# ==========================================
final_prompt = None
is_audio_mode = False
audio_bytes_data = None

if user_text:
    final_prompt = user_text
elif audio_data is not None and 'bytes' in audio_data:
    final_prompt = "[음성 질문 수신됨]"
    is_audio_mode = True
    audio_bytes_data = audio_data['bytes']

if final_prompt:
    # 사용자 메시지 등록
    st.session_state.messages.append({"role": "user", "content": final_prompt})

    # Gemini API 응답 생성
    with chat_container:
        with st.chat_message("user"):
            st.markdown(final_prompt)

        with st.chat_message("assistant"):
            if not client:
                st.error("API 키 설정이 올바르지 않습니다. 서버 환경변수를 확인해 주세요.")
            else:
                msg_placeholder = st.empty()
                try:
                    sys_prompt = """
                    당신은 한단제어기술의 FA, PLC, 모션 제어, 감속기, 인버터 등 
                    산업 자동화 제품 전문 AI 기술지원 비서입니다.
                    엔지니어의 현장 질문에 대해 매뉴얼과 첨부자료를 바탕으로 명확하고 신속하게 답변하세요.
                    """
                    
                    # 입력 모드(음성 / 텍스트) 구분 처리
                    if is_audio_mode:
                        contents_payload = [
                            sys_prompt,
                            types.Part.from_bytes(data=audio_bytes_data, mime_type="audio/wav")
                        ]
                    else:
                        contents_payload = final_prompt

                    response = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=contents_payload,
                        config=types.GenerateContentConfig(
                            system_instruction=sys_prompt
                        )
                    )
                    
                    ans_text = response.text
                    msg_placeholder.markdown(ans_text)

                    # --- gTTS 음성 변환 (음성 재생 파일 생성) ---
                    tts = gTTS(text=ans_text, lang='ko')
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    audio_out_bytes = fp.read()

                    # 메시지 내역에 텍스트 및 음성 저장
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": ans_text,
                        "audio": audio_out_bytes
                    })

                    st.rerun()

                except Exception as e:
                    st.error(f"답변 생성 오류: {e}")