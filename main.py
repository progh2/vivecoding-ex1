import streamlit as st

# 웹 앱의 제목 설정
st.title("➡️ 수평 정렬 Streamlit 환영 앱") 

# 1. 입력창과 버튼을 담을 컨테이너 생성
# st.empty()를 사용하여 입력창과 버튼이 포함될 하나의 영역을 정의합니다.
container = st.container()

with container:
    # 2. 컨테이너 안에 2개의 컬럼 생성 (입력창: 버튼 = 3:1 비율)
    col1, col2 = st.columns([3, 1])
    
    # 첫 번째 컬럼: 텍스트 입력창
    with col1:
        # st.session_state를 사용하여 입력 값을 저장, 버튼 클릭 후에도 값이 유지되도록 합니다.
        if 'user_name' not in st.session_state:
            st.session_state.user_name = "방문자"
            
        user_name = st.text_input(
            "당신의 이름을 입력해주세요:", 
            key="name_input_box",
            label_visibility="collapsed" # 레이블 숨김으로 깔끔하게 정렬
        )
    
    # 두 번째 컬럼: '입력' 버튼
    with col2:
        # 버튼을 입력창과 수평하게 정렬하기 위해 버튼 위에 약간의 공간(placeholder)을 추가할 수 있습니다.
        # st.write() 대신 st.button()만 사용해도 되지만, 세로 정렬이 완벽히 맞지 않을 경우 CSS나 st.write('\n') 등으로 조정할 수 있습니다.
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
