import streamlit as st
import pandas as pd

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="MBTI World Map (Semantic UI)",
    page_icon="🌏",
    layout="wide"
)

# --- 2. Semantic UI CDN 및 커스텀 CSS 주입 ---
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css">
    <style>
        /* 스트림릿 기본 컨테이너와 겹치지 않도록 조정 */
        .main .block-container {
            padding-top: 2rem;
        }
        /* Semantic UI 폰트 적용을 위한 설정 */
        body {
            font-family: 'Lato', 'Helvetica Neue', Arial, Helvetica, sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. 데이터 로드 ---
@st.cache_data
def load_data():
    try:
        # 파일이 존재하는지 확인하고 로드
        df = pd.read_csv("countriesMBTI_16types.csv")
        return df
    except FileNotFoundError:
        st.error("CSV 파일을 찾을 수 없습니다. 'countriesMBTI_16types.csv' 파일이 있는지 확인해주세요.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"데이터 로드 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()

df = load_data()

# --- 4. MBTI 정보 정의 ---
mbti_info = {
    "ISTJ": ("청렴결백 논리주의자", "blue"),
    "ISFJ": ("용감한 수호자", "blue"),
    "INFJ": ("선의의 옹호자", "green"),
    "INTJ": ("용의주도한 전략가", "violet"),
    "ISTP": ("만능 재주꾼", "yellow"),
    "ISFP": ("호기심 많은 예술가", "yellow"),
    "INFP": ("열정적인 중재자", "green"),
    "INTP": ("논리적인 사색가", "violet"),
    "ESTP": ("모험을 즐기는 사업가", "orange"),
    "ESFP": ("자유로운 영혼의 연예인", "orange"),
    "ENFP": ("재기발랄한 활동가", "green"),
    "ENTP": ("뜨거운 논쟁을 즐기는 변론가", "violet"),
    "ESTJ": ("엄격한 관리자", "teal"),
    "ESFJ": ("사교적인 외교관", "teal"),
    "ENFJ": ("정의로운 사회운동가", "green"),
    "ENTJ": ("대담한 통솔자", "violet")
}

# --- 5. 화면 구성 (UI) ---

# 5-1. 헤더
st.markdown("""
    <h2 class="ui center aligned icon header">
      <i class="circular globe icon"></i>
      MBTI Global Statistics
      <div class="sub header">당신의 성격 유형은 어느 나라에서 가장 흔할까요?</div>
    </h2>
    <div class="ui divider"></div>
""", unsafe_allow_html=True)

# 5-2. 사용자 입력 (MBTI 선택)
mbti_types = sorted(list(mbti_info.keys()))
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    selected_mbti = st.selectbox(
        "당신의 MBTI를 선택해주세요",
        options=["선택해주세요"] + mbti_types,
        index=0
    )

# --- 6. 로직 및 결과 표시 ---

if selected_mbti == "선택해주세요":
    # 초기 화면 안내 메시지
    st.markdown("""
        <div class="ui info message">
          <div class="header">
            아직 선택된 MBTI가 없습니다.
          </div>
          <p>위 목록에서 당신의 MBTI를 선택하면 전 세계 통계 정보를 보여드립니다.</p>
        </div>
    """, unsafe_allow_html=True)

else:
    if not df.empty:
        desc, color_theme = mbti_info[selected_mbti]
        
        # 데이터 분석
        sorted_df = df[['Country', selected_mbti]].sort_values(by=selected_mbti, ascending=False)
        top_country = sorted_df.iloc[0]['Country']
        top_value = sorted_df.iloc[0][selected_mbti]
        avg_value = sorted_df[selected_mbti].mean()
        top_10_df = sorted_df.head(10).set_index('Country')

        # 6-1. 선택된 MBTI 설명
        st.markdown(f"""
            <div class="ui raised segment">
                <a class="ui {color_theme} ribbon label">{selected_mbti}</a>
                <span><b>{desc}</b> 성향을 선택하셨습니다.</span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 6-2. 주요 통계 보여주기
        st.markdown(f"""
            <div class="ui three statistics">
              <div class="statistic">
                <div class="value">
                  <i class="trophy icon"></i> {top_country}
                </div>
                <div class="label">
                  가장 비율이 높은 나라
                </div>
              </div>
              <div class="statistic">
                <div class="value">
                  {top_value:.1%}
                </div>
                <div class="label">
                  해당 국가 비율
                </div>
              </div>
              <div class="statistic">
                <div class="value">
                  {avg_value:.1%}
                </div>
                <div class="label">
                  전 세계 평균
                </div>
              </div>
            </div>
            <br>
        """, unsafe_allow_html=True)

        # 6-3. 맞춤형 멘트
        diff = top_value - avg_value
        
        st.markdown(f"""
            <div class="ui icon positive message">
              <i class="plane icon"></i>
              <div class="content">
                <div class="header">
                  여행 추천: {top_country}
                </div>
                <p><b>{top_country}</b>에는 당신과 같은 <b>{selected_mbti}</b> 성향의 사람들이 
                전 세계 평균보다 약 <b>{diff:.1%}p</b> 더 많이 살고 있습니다.<br>
                마음이 잘 통하는 친구들을 만날 확률이 높은 이곳으로 떠나보는 건 어떨까요?</p>
              </div>
            </div>
        """, unsafe_allow_html=True)

        # 6-4. 차트
        st.subheader(f"📊 {selected_mbti} 비율 상위 10개국")
        st.bar_chart(top_10_df, color="#FF4B4B")

        # 6-5. 데이터 표 (에러 수정됨)
        with st.expander("📋 전체 데이터 목록 보기"):
            # .background_gradient(...) 제거하여 ImportError 방지
            # 숫자 포맷팅만 적용
            st.dataframe(
                sorted_df.style.format({selected_mbti: "{:.2%}"})
            )
