import streamlit as st
import pandas as pd

# 페이지 기본 설정
st.set_page_config(
    page_title="MBTI 세계 지도",
    page_icon="🌏",
    layout="wide"
)

# --- 1. 데이터 로드 및 캐싱 ---
@st.cache_data
def load_data():
    # 업로드된 파일명을 그대로 사용합니다.
    try:
        df = pd.read_csv("countriesMBTI_16types.csv")
        return df
    except FileNotFoundError:
        st.error("CSV 파일을 찾을 수 없습니다. 'countriesMBTI_16types.csv' 파일을 같은 폴더에 넣어주세요.")
        return pd.DataFrame()

df = load_data()

# --- 2. MBTI 설명 데이터 (간단한 딕셔너리) ---
mbti_info = {
    "ISTJ": "사실을 중시하는 믿음직한 현실주의자 (청렴결백 논리주의자)",
    "ISFJ": "주변 사람을 보호할 준비가 된 헌신적이고 성실한 수호자 (용감한 수호자)",
    "INFJ": "조용하고 신비로우며 샘솟는 영감으로 지칠 줄 모르는 이상주의자 (선의의 옹호자)",
    "INTJ": "상상력이 풍부하며 철두철미한 계획을 세우는 전략가 (용의주도한 전략가)",
    "ISTP": "대담하고 현실적인 성향으로 도구 사용에 능숙한 탐험형 (만능 재주꾼)",
    "ISFP": "항상 새로운 경험을 추구하는 유연하고 매력적인 예술가 (호기심 많은 예술가)",
    "INFP": "항상 선을 행할 준비가 되어 있는 부드럽고 친절한 이타주의자 (열정적인 중재자)",
    "INTP": "끊임없이 새로운 지식을 갈망하는 혁신적인 발명가 (논리적인 사색가)",
    "ESTP": "위험을 기꺼이 감수하는 영리하고 에너지 넘치는 활동가 (모험을 즐기는 사업가)",
    "ESFP": "즉흥적이고 넘치는 에너지와 열정으로 주변을 즐겁게 하는 연예인 (자유로운 영혼의 연예인)",
    "ENFP": "열정적이고 창의적인 성격으로 긍정적으로 삶을 바라보는 사교적인 활동가 (재기발랄한 활동가)",
    "ENTP": "지적인 도전을 두려워하지 않는 똑똑한 호기심형 (뜨거운 논쟁을 즐기는 변론가)",
    "ESTJ": "사물과 사람을 관리하는 데 뛰어난 능력을 지닌 경영자 (엄격한 관리자)",
    "ESFJ": "타인을 향한 세심한 관심과 사교적인 성향으로 인기가 많은 조력자 (사교적인 외교관)",
    "ENFJ": "청중을 사로잡고 의욕을 불어넣는 카리스마 넘치는 지도자 (정의로운 사회운동가)",
    "ENTJ": "대담하고 상상력이 풍부하며 강력한 의지의 지도자 (대담한 통솔자)"
}

# --- 3. UI 구성 ---

st.title("🌏 당신의 MBTI는 어디서 가장 환영받을까요?")
st.markdown("---")

# MBTI 리스트 생성 (알파벳 순 정렬)
mbti_types = sorted(list(mbti_info.keys()))

# 사용자 선택 (기본값은 None)
selected_mbti = st.selectbox(
    "당신의 MBTI를 선택해주세요 👇",
    options=["선택해주세요"] + mbti_types,
    index=0
)

# --- 4. 로직 처리 ---

if selected_mbti == "선택해주세요":
    # 선택되지 않았을 때의 화면
    st.info("👋 위 드롭다운 메뉴에서 자신의 MBTI를 선택하면 분석 결과가 나타납니다!")
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=100) # 예시 이미지 (로고)

else:
    # MBTI가 선택되었을 때
    if not df.empty:
        # 1) 기본 설명 섹션
        st.header(f"✨ {selected_mbti}")
        st.subheader(mbti_info[selected_mbti])
        
        st.divider()

        # 2) 데이터 분석
        # 해당 MBTI 컬럼만 가져와서 내림차순 정렬
        sorted_df = df[['Country', selected_mbti]].sort_values(by=selected_mbti, ascending=False)
        
        # 주요 통계 산출
        top_country = sorted_df.iloc[0]['Country']
        top_value = sorted_df.iloc[0][selected_mbti]
        avg_value = sorted_df[selected_mbti].mean()
        
        # 나의 비율이 가장 높은 나라 TOP 10 데이터
        top_10_df = sorted_df.head(10).set_index('Country')

        # 3) 통계 보여주기 (컬럼 나누기)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="🏆 가장 비율이 높은 나라", value=top_country)
        with col2:
            st.metric(label="📊 해당 국가의 비율", value=f"{top_value:.1%}")
        with col3:
            st.metric(label="🌍 전 세계 평균 비율", value=f"{avg_value:.1%}", delta=f"{(top_value - avg_value):.1%}p 차이")

        # 4) 맞춤형 멘트 생성
        st.success(f"""
        💡 **재미있는 사실**:  
        **{selected_mbti}** 유형은 전 세계 평균적으로 약 **{avg_value:.1%}** 분포되어 있습니다.  
        하지만 **{top_country}**에서는 무려 **{top_value:.1%}**의 사람들이 당신과 같은 성향을 가지고 있네요!  
        다음 여행지로 **{top_country}** 어떠신가요? 마음이 잘 맞는 친구들을 많이 만날지도 몰라요! ✈️
        """)

        # 5) 차트 시각화
        st.subheader(f"📈 {selected_mbti} 비율이 가장 높은 국가 TOP 10")
        st.bar_chart(top_10_df, color="#FF4B4B") # 스트림릿 기본 차트 사용

        # 6) 원본 데이터 보기 (옵션)
        with st.expander("전체 국가 데이터 보기"):
            st.dataframe(sorted_df.style.format({selected_mbti: "{:.2%}"}))
