import streamlit as st
import base64

# --- 1. 배경 이미지 목록 및 설정 ---
# **중요:** 이 이미지 URL들을 실제 고양이 이미지 URL 목록으로 교체해야 합니다.
# 배경으로 사용될 고양이 이미지 URL 리스트
CAT_IMAGE_URLS = [
    "https://cdn.pixabay.com/photo/2017/11/09/21/41/cat-2934720_1280.jpg", # 고양이 1
    "https://cdn.pixabay.com/photo/2020/09/01/21/11/cat-5536411_1280.jpg", # 고양이 2
    "https://cdn.pixabay.com/photo/2016/03/27/21/20/cat-1283287_1280.jpg", # 고양이 3
    "https://cdn.pixabay.com/photo/2017/02/20/18/03/cat-2083492_1280.jpg", # 고양이 4
]

# 한 이미지가 표시되는 시간 (초)
TIME_PER_IMAGE = 5 # 5초마다 이미지 변경

# 전체 애니메이션 주기 (초)
TOTAL_ANIMATION_TIME = len(CAT_IMAGE_URLS) * TIME_PER_IMAGE

# --- 2. CSS 애니메이션 키프레임 생성 ---
# 키프레임을 동적으로 생성하여 배경 이미지를 순환시킵니다.
keyframes_css = ""
for i, url in enumerate(CAT_IMAGE_URLS):
    # 각 이미지의 시작 및 종료 지점 계산 (백분율)
    start_percent = (i / len(CAT_IMAGE_URLS)) * 100
    end_percent = ((i + 1) / len(CAT_IMAGE_URLS)) * 100 - 0.01

    # CSS 배경 이미지 경로를 URL로 설정
    image_css_url = f"url('{url}')"
    
    # 키프레임 정의
    keyframes_css += f"""
        {start_percent:.2f}% {{ background-image: {image_css_url}; }}
        {end_percent:.2f}% {{ background-image: {image_css_url}; }}
    """

# --- 3. Streamlit에 CSS 주입 ---
st.markdown(
    f"""
    <style>
    /* 배경 이미지를 순환시키는 CSS 애니메이션 */
    @keyframes slideshow {{
        {keyframes_css}
    }}

    .stApp {{
        /* 애니메이션 적용: 주기, 선형, 무한 반복 */
        animation: slideshow {TOTAL_ANIMATION_TIME}s linear infinite;
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        /* 배경 이미지 변경 시 부드러운 전환을 위한 트랜지션 (선택 사항) */
        transition: background-image 1s ease-in-out; 
    }}
    
    /* 텍스트 가독성을 위한 스타일 (흰색 텍스트와 그림자) */
    .stTextInput > label, .stButton > button, h1, h2, h3, .stSuccess {{
        color: white !important; 
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }}
    .stButton > button {{
        background-color: #ff9900;
        border-radius: 12px;
        padding: 8px 16px;
        font-size: 1.2em;
        border: none;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 웹 앱의 제목 설정 (흰색으로 보이도록 CSS에 설정함)
st.title("🔄 배경 슬라이드쇼 고양이 앱") 

# --- 4. 사용자 입력 및 버튼 로직 (기존 유지) ---

container = st.container()

with container:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if 'user_name' not in st.session_state:
            st.session_state.user_name = "방문자"
            
        user_name = st.text_input(
            "당신의 이름을 입력해주세요:", 
            key="name_input_box",
            value=st.session_state.user_name,
            label_visibility="collapsed" 
        )
    
    with col2:
        st.write("") # 수직 정렬을 위한 공간 확보
        # 고양이 발바닥 이모지 🐾를 버튼 텍스트에 추가
        button_clicked = st.button("🐾 입력", key="submit_button")

# --- 메시지 출력 영역 ---
if button_clicked:
    if user_name:
        greeting_message = f"**Hello World!** {user_name}님, Streamlit 앱에 오신 것을 환영합니다."
        
        st.balloons() # 애니메이션 효과
        
        # 메시지 출력 (입력창과 버튼 아래에 표시)
        st.success(greeting_message)
    else:
        st.warning("이름을 입력한 후 버튼을 눌러주세요.")
