import streamlit as st

# 웹 앱의 제목 설정
st.title("✨ 인터랙티브 Streamlit 환영 앱") 

# 1. 사용자 이름 입력 받기
user_name = st.text_input("당신의 이름을 입력해주세요:", "방문자")

# 2. '입력' 버튼 생성
# st.button() 함수는 사용자가 클릭할 때 True를 반환합니다.
if st.button("결과 보기 (입력)"):
    # 버튼이 클릭되었을 때만 이 블록의 코드가 실행됩니다.
    
    # 3. 환영 메시지 생성
    if user_name:
        greeting_message = f"**Hello World!** {user_name}님, Streamlit 앱에 오신 것을 환영합니다."
        
        # 4. 애니메이션 효과 (축하 폭죽)
        # st.balloons() 또는 st.snow()를 사용하여 재미있는 애니메이션을 추가할 수 있습니다.
        st.balloons()
        
        # 5. 메시지 출력
        st.success(greeting_message)
    else:
        # 이름이 비어 있을 경우 처리
        st.warning("이름을 입력한 후 버튼을 눌러주세요.")
