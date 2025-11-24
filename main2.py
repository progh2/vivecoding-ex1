import streamlit as st

# --- 배경 이미지 설정 ---
# 로컬 이미지 파일을 사용하거나 웹상의 이미지 URL을 사용할 수 있습니다.
# 여기서는 예시로 고양이 이미지 URL을 사용합니다.
# 로컬 이미지를 사용하려면, 이미지 파일을 프로젝트 폴더에 넣고 경로를 지정해주세요.
# 예: IMAGE_URL = "file:///app/cat.jpg" (Docker 컨테이너 등) 또는 "cat.jpg"
CAT_IMAGE_URL = "https://cdn.pixabay.com/photo/2017/11/09/21/41/cat-2934720_1280.jpg" # 예시 고양이 이미지 URL

# CSS를 사용하여 배경 이미지 설정
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url({CAT_IMAGE_URL});
        background-size: cover; # 이미지가 화면 전체를 덮도록 설정
        background-repeat: no-repeat; # 이미지 반복 방지
        background-attachment: fixed; # 스크롤해도 배경 고정
        background-position: center; # 이미지를 중앙에 배치
    }}
    .stTextInput > label, .stButton > button {{
        color: black; /* 입력창 레이블과 버튼 텍스트 색상 조정 (배경 대비) */
        font-weight: bold;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 웹 앱의 제목 설정
st.title("🐱 헬로 월드 고양이 배경 앱") 

# 입력창과 버튼을 담을 컨테이너 생성
# st.empty()를 사용하여 입력창과 버튼이 포함될 하나의 영역을 정의합니다.
container = st.container()

with container:
    # 컨테이너 안에 2개의 컬럼 생성 (입력창: 버튼 = 3:1 비율)
    col1, col2 = st.columns([3, 1])
    
    # 첫 번째 컬럼: 텍스트 입력창
    with col1:
        # st.session_state를 사용하여 입력 값을 저장, 버튼 클릭 후에도 값이 유지되도록 합니다.
        if 'user_name' not in st.session_state:
            st.session_state.user_name = "방문자"
            
        user_name = st.text_input(
            "당신의 이름을 입력해주세요:", 
            key="name_input_box",
            value=st.session_state.user_name, # 기본값 설정
            label_visibility="collapsed" # 레이블 숨김으로 깔끔하게 정렬
        )
    
    # 두 번째 컬럼: '입력' 버튼
    with col2:
        # 버튼을 입력창과 수평하게 정렬하기 위해 버튼 위에 약간의 공간(placeholder)을 추가할 수 있습니다.
        st.write("") # 간단한 수직 정렬을 위한 공간 확보
        button_clicked = st.button("입력", key="submit_button")

# --- 메시지 출력 영역 ---
# 3. 버튼이 클릭되었을 때 메시지 표시
if button_clicked:
    # 입력된 이름으로 메시지 생성
    if user_name:
        greeting_message = f"**Hello World!** {user_name}님, Streamlit 앱에 오신 것을 환영합니다."
        
        # 애니메이션 효과
        st.balloons()
        
        # 메시지 출력 (입력창과 버튼 아래에 표시)
        st.success(greeting_message)
    else:
        st.warning("이름을 입력한 후 버튼을 눌러주세요.")
