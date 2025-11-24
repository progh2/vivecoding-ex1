import streamlit as st

# 웹 앱의 제목 설정
st.title("간단한 헬로 월드 Streamlit 앱") 

# 1. 사용자 이름 입력 받기
# st.text_input() 함수는 사용자로부터 텍스트를 입력받는 입력 필드를 생성합니다.
user_name = st.text_input("당신의 이름을 입력해주세요:", "방문자")

# 2. 메시지 생성 및 표시
if user_name:
    # f-string을 사용하여 입력받은 이름과 "헬로 월드" 메시지를 결합
    greeting_message = f"**Hello World!** {user_name}님, Streamlit 앱에 오신 것을 환영합니다."
    
    # st.write() 함수는 텍스트나 다른 Streamlit 요소를 표시합니다.
    st.write(greeting_message)

# 참고: st.success()나 st.info() 등을 사용하여 더 시각적인 메시지를 표시할 수도 있습니다.
# st.success(f"성공적으로 환영 메시지를 표시했습니다: {user_name}")
