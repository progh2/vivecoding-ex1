import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from extra_streamlit_components import TabBar, Tab, Card
from streamlit_extras.colored_header import colored_header
from streamlit_extras.app_logo import add_logo
from streamlit_extras.let_it_rain import rain

# ----------------- 1. 설정 및 데이터 로드 -----------------
# 페이지 설정
st.set_page_config(
    page_title="🌟 MBTI 세계관 탐험기 🌎",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 파일 로드 (사용자가 업로드한 파일 이름 사용)
FILE_PATH = "countriesMBTI_16types.csv"
try:
    df = pd.read_csv(FILE_PATH)
    # 첫 번째 컬럼 이름을 'Country'로 확실하게 설정
    if df.columns[0] != 'Country':
        df = df.rename(columns={df.columns[0]: 'Country'})
    
    # MBTI 유형 리스트 생성 (Country 컬럼 제외)
    MBTI_TYPES = df.columns.tolist()[1:]
except FileNotFoundError:
    st.error(f"첨부 파일 '{FILE_PATH}'을 찾을 수 없습니다. 파일 이름을 확인해주세요.")
    st.stop()
except Exception as e:
    st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
    st.stop()


# ----------------- 2. MBTI 유형별 설명 및 멘트 -----------------

MBTI_INFO = {
    "INTJ": {"icon": "💡", "desc": "용의주도한 전략가", "ment": "**INTJ**! 분석적이고 독립적인 당신은 **세계를 설계하는 건축가**와 같습니다. 미래를 향한 명확한 비전으로 목표를 달성할 능력이 있어요! 🚀"},
    "INTP": {"icon": "🧠", "desc": "논리적인 사색가", "ment": "**INTP**! 지적인 호기심이 넘치는 당신은 **아이디어의 끊임없는 샘**입니다. 복잡한 문제를 풀어내는 즐거움을 아는 진정한 탐험가! 🌌"},
    "ENTJ": {"icon": "👑", "desc": "대담한 통솔자", "ment": "**ENTJ**! 카리스마 넘치는 리더십의 소유자! **목표를 향해 거침없이 나아가는 장군**처럼 팀을 이끌어 비전을 현실로 만들 능력이 있습니다! 🌟"},
    "ENTP": {"icon": "🌪️", "desc": "뜨거운 논쟁을 즐기는 변론가", "ment": "**ENTP**! 기발한 아이디어와 뛰어난 언변의 소유자! **세상의 고정관념을 깨부수는 혁신가**의 역할을 멋지게 해낼 거예요! ✨"},
    "INFJ": {"icon": "😇", "desc": "선의의 옹호자", "ment": "**INFJ**! 깊은 통찰력과 따뜻한 마음을 가진 당신은 **세상의 등불**과 같습니다. 사람들의 성장을 돕고 의미있는 변화를 만드는 선한 영향력! 💖"},
    "INFP": {"icon": "🦄", "desc": "열정적인 중재자", "ment": "**INFP**! 이상을 추구하고 진정한 가치를 중요시하는 당신은 **영혼의 시인**입니다. 내면의 깊은 울림으로 세상을 더 아름답게 만들 수 있어요! 🌿"},
    "ENFJ": {"icon": "🫂", "desc": "정의로운 사회 운동가", "ment": "**ENFJ**! 사람들에게 영감을 주고 동기를 부여하는 **타고난 멘토**입니다. 뛰어난 공감 능력으로 모두가 함께 성장하는 세상을 꿈꿉니다! 🌈"},
    "ENFP": {"icon": "☀️", "desc": "재기발랄한 활동가", "ment": "**ENFP**! 에너지가 넘치고 창의적인 당신은 **삶을 축제로 만드는 주인공**입니다. 새로운 가능성을 끊임없이 탐색하는 자유로운 영혼! 🎉"},
    "ISTJ": {"icon": "📝", "desc": "청렴결백한 논리주의자", "ment": "**ISTJ**! 현실적이고 책임감이 강한 당신은 **사회의 굳건한 기둥**입니다. 당신의 정확성과 헌신은 언제나 믿음을 줍니다! 🏛️"},
    "ISFJ": {"icon": "🛡️", "desc": "용감한 수호자", "ment": "**ISFJ**! 타인의 필요를 놓치지 않는 따뜻한 당신은 **가장 든든한 지원군**입니다. 조용하지만 강한 헌신으로 주변을 지켜줍니다! 🏡"},
    "ESTJ": {"icon": "💼", "desc": "엄격한 관리자", "ment": "**ESTJ**! 명확한 규칙과 효율성을 중시하는 당신은 **조직의 엔진**입니다. 질서를 확립하고 계획을 완벽하게 실행해내는 능력자! 🎯"},
    "ESFJ": {"icon": "🥳", "desc": "사교적인 외교관", "ment": "**ESFJ**! 사람들과의 관계를 소중히 여기는 당신은 **모두를 하나로 엮는 접착제**입니다. 당신의 친화력은 최고의 강점입니다! 🎈"},
    "ISTP": {"icon": "🔧", "desc": "만능 재주꾼", "ment": "**ISTP**! 손으로 만들고 직접 경험하는 것을 즐기는 당신은 **현실 문제 해결사**입니다. 어떤 도구든 능숙하게 다루는 멋진 재주꾼! 🛠️"},
    "ISFP": {"icon": "🌸", "desc": "호기심 많은 예술가", "ment": "**ISFP**! 아름다움을 추구하고 순간을 즐기는 당신은 **자유로운 예술혼**입니다. 당신의 감각적인 표현은 세상을 풍요롭게 만듭니다! 🎨"},
    "ESTP": {"icon": "🏎️", "desc": "모험을 즐기는 사업가", "ment": "**ESTP**! 에너지와 스릴을 즐기는 당신은 **행동파의 정점**입니다. 지금 당장, 눈 앞의 기회를 놓치지 않는 민첩함이 빛납니다! 💥"},
    "ESFP": {"icon": "🎤", "desc": "자유로운 연예인", "ment": "**ESFP**! 주변을 즐겁게 만들 줄 아는 당신은 **파티의 중심**입니다. 밝고 긍정적인 에너지로 모두에게 활력을 불어넣습니다! 🌟"}
}

# ----------------- 3. 메인 앱 레이아웃 -----------------

# 제목 및 로고
st.markdown("<h1 style='text-align: center; color: #4B0082;'>🌟 MBTI 세계관 탐험기 🌎</h1>", unsafe_allow_html=True)
st.markdown("---")

# 사이드바 메뉴 (option_menu 라이브러리 사용)
with st.sidebar:
    st.subheader("🔎 MBTI 유형 선택")
    # '선택 안함' 옵션을 추가하여 초기 상태를 표현
    selected_mbti = option_menu(
        menu_title=None,
        options=["선택 안함"] + MBTI_TYPES,
        icons=["house"] + [MBTI_INFO[mbti]["icon"] for mbti in MBTI_TYPES],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#0288d1"},
        }
    )

# ----------------- 4. 선택 결과 처리 및 표시 -----------------

if selected_mbti == "선택 안함":
    # 4-1. 초기 접속 시 메시지 (요청 4번)
    st.info("👋 **환영합니다!** 웹 앱 사용을 위해 왼쪽 사이드바에서 **MBTI 유형**을 선택해주세요!")
    
    # 삐까뻔쩍함을 위한 빗방울 효과 (streamlit-extras)
    rain(
        emoji="✨",
        font_size=50,
        falling_speed=5,
        animation_length="3s",
    )
    
    st.image("https://images.unsplash.com/photo-1518621736915-f5f4b00868d4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1740&q=80", 
             caption="다양한 유형을 탐험해 보세요!", use_column_width=True)

else:
    # 4-2. MBTI가 선택되었을 때
    mbti_type = selected_mbti
    info = MBTI_INFO[mbti_type]
    
    # 선택된 MBTI에 대한 헤더 (streamlit-extras)
    colored_header(
        label=f"{info['icon']} **{mbti_type}** : {info['desc']}",
        description=f"선택하신 MBTI 유형 **{mbti_type}**에 대한 분석 정보입니다.",
        color_name="blue-70",
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        # MBTI 설명 및 멘트 (요청 2, 3번)
        st.subheader(f"✨ 당신을 위한 멘트")
        st.markdown(f"> {info['ment']}")
        
        # 간단한 통계 정보 카드 (extra-streamlit-components)
        st.subheader(f"📊 전 세계적 비율")
        
        # 해당 MBTI의 평균 비율 계산
        avg_ratio = df[mbti_type].mean() * 100
        
        st.metric(
            label=f"{mbti_type} 전 세계 평균 비율",
            value=f"{avg_ratio:.2f}%",
            delta=f"16가지 유형 중 평균보다 {'높습니다' if avg_ratio > 100/16 else '낮습니다'}",
            delta_color="normal"
        )
        
    with col2:
        # 4-3. 데이터 시각화 (요청 3번)
        st.subheader(f"🌎 국가별 {mbti_type} 비율 통계")
        
        # 선택된 MBTI 컬럼을 기준으로 내림차순 정렬
        top_n = 15
        plot_df = df.sort_values(by=mbti_type, ascending=False).head(top_n)
        
        # Plotly를 사용한 막대 그래프 (인터랙티브)
        fig = px.bar(
            plot_df,
            x=mbti_type,
            y='Country',
            orientation='h',
            title=f"MBTI {mbti_type} 유형 비율이 높은 상위 {top_n}개 국가",
            labels={mbti_type: f"{mbti_type} 비율", "Country": "국가"},
            color=mbti_type,
            color_continuous_scale=px.colors.sequential.Viridis,
            height=600
        )
        
        # 레이아웃 개선
        fig.update_layout(
            xaxis_tickformat=".2%",
            yaxis={'categoryorder':'total ascending'}
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.caption(f"**데이터 출처:** 첨부하신 `{FILE_PATH}` 파일 기반")


# ----------------- 5. 추가 정보 표시 -----------------
with st.expander("🛠️ 사용된 라이브러리 목록"):
    st.write("""
    이 앱은 아래의 라이브러리를 사용하여 개발되었습니다:
    - **`streamlit`**: 웹 앱의 기본 프레임워크
    - **`pandas`**: 데이터 처리 및 분석
    - **`plotly`**: 멋진 인터랙티브 데이터 시각화
    - **`streamlit-option-menu`**: 사이드바에 깔끔한 메뉴 구현
    - **`extra-streamlit-components`**: 아이콘 및 카드 구성
    - **`streamlit-extras`**: 추가적인 UI/UX 개선 기능 (헤더, 이모지 비, 로고 등)
    """)
