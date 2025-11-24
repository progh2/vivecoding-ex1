import streamlit as st

# 웹 앱의 제목 설정
st.title("↔️ 가로 정렬된 입력 및 버튼 앱") 

# 1. 화면을 두 개의 열(Column)로 나눕니다.
# 첫 번째 열(col1)은 너비를 3으로, 두 번째 열(col2)은 너비를 1로 설정하여 입력 필드가 더 넓게 보이도록 합니다.
col1, col2 = st.columns([3, 1])

# 2. 첫 번째 열(col1)에 사용자 이름 입력 필드를 배치합니다.
# 주의: st.text_input()은 입력 값을 반환하므로, 반드시 변수에 할당해야 합니다.
with col1:
    user_name = st.text_input("당신의 이름을 입력해주세요:", "방문자", label_visibility="collapsed") 
    # label_visibility="collapsed"를 사용하여 기본 라벨을 숨겨 공간을 절약합니다.

# 3. 두 번째 열(col2)에 '입력' 버튼을 배치합니다.
with col2:
    # 컬럼 내에서 버튼을 입력창과 수직으로 정렬하기 위해 st.button() 위에 st.empty() 등을 사용하여 공간을 확보할 필요가 있지만,
    # 여기서는 간단하게 버튼을 바로 배치합니다.
    # 하지만 Streamlit은 버튼과 입력창의 높이가 다르기 때문에, 버튼을 클릭하기 전에
    # 입력 필드와 시각적으로 맞추기 위해 약간의 트릭(예: st.write('<style>...</style>', unsafe_allow_html=True) 또는 st.empty() 후 버튼 배치)이 필요할 수 있습니다.
    # 여기서는 기본 정렬을 사용합니다.
    st.write("") # 이 줄은 버튼을 입력창과 시각적으로 조금 더 맞추기 위한 빈 줄입니다.
    if st.button("입력"):
        # 4. 버튼이 클릭되었을 때의 로직
        if user_name:
            greeting_message = f"**Hello World!** {user_name}님, Streamlit 앱에 오신 것을 환영합니다."
            st.success(greeting_message)
            st.balloons()
        else:
            st.warning("이름을 입력한 후 버튼을 눌러주세요.")

# 5. 결과 메시지는 컬럼 밖, 즉 원래 위치인 입력창 아래에 표시되도록 합니다.
# 이전에 사용자가 입력 필드에 이름을 입력했는지 확인하고 메시지를 표시하는 코드를 추가합니다.
