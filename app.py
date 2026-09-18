import streamlit as st
from ai_helper import ask_ai

# 페이지 설정
st.set_page_config(
    page_title="여행 하루 코스",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
if "mode" not in st.session_state:
    st.session_state.mode = None
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "selected_style" not in st.session_state:
    st.session_state.selected_style = None
if "first_place" not in st.session_state:
    st.session_state.first_place = None
if "final_itinerary" not in st.session_state:
    st.session_state.final_itinerary = None
if "final_cost" not in st.session_state:
    st.session_state.final_cost = None

# 커스텀 CSS 스타일
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');

    * {
        font-family: 'Noto Sans KR', sans-serif !important;
    }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #2d2d3d 0%, #3d4856 100%);
        min-height: 100vh;
        background-attachment: fixed;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #3d4856 0%, #2d2d3d 100%);
        color: #e8e8e8;
    }

    [data-testid="stSidebar"] > * {
        color: #e8e8e8;
    }

    [data-testid="stSidebar"] label {
        color: #e8e8e8 !important;
        font-size: 1.1em !important;
        font-weight: 500 !important;
        line-height: 1.6 !important;
    }

    .main-title {
        text-align: center;
        font-size: 4em;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        letter-spacing: 1px;
    }

    .subtitle {
        text-align: center;
        font-size: 1.5em;
        color: #b0b0b0;
        margin-bottom: 40px;
        font-weight: 500;
        line-height: 1.8;
    }

    .section-title {
        font-size: 2.4em;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 25px;
        border-bottom: 3px solid #667eea;
        padding-bottom: 15px;
        color: #e8e8e8;
        line-height: 1.4;
    }

    .highlight-box {
        background: linear-gradient(135deg, #3d4856 0%, #2d3644 100%);
        padding: 30px;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin: 25px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        color: #e8e8e8;
        line-height: 1.9;
    }

    .highlight-box h1 {
        font-size: 1.8em;
        margin: 25px 0 15px 0;
        color: #7b68ee;
        font-weight: 700;
        line-height: 1.6;
    }

    .highlight-box h2 {
        font-size: 1.5em;
        margin: 20px 0 12px 0;
        color: #9d8fdb;
        font-weight: 600;
        line-height: 1.6;
    }

    .highlight-box h3 {
        font-size: 1.2em;
        margin: 15px 0 10px 0;
        color: #c0c0c0;
        font-weight: 600;
    }

    .highlight-box p, .highlight-box li {
        color: #e8e8e8;
        font-size: 1.05em;
        line-height: 1.9;
        margin: 10px 0;
    }

    .highlight-box strong {
        color: #667eea;
        font-weight: 700;
    }

    button {
        font-size: 1.15em !important;
        padding: 15px 20px !important;
        font-weight: 600 !important;
        line-height: 1.6 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🛫 나의 여행 계획 🌍</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">설렘 가득한 하루 여행을 준비하세요!</div>', unsafe_allow_html=True)

# 사이드바에서 입력받기
with st.sidebar:
    st.markdown("### ✈️ 탑승 정보")
    st.markdown("---")

    city = st.text_input(
        "🏙️ 목적지",
        placeholder="예: 서울, 부산, 제주",
        help="어디로 가고 싶으신가요?"
    )

    weather = st.selectbox(
        "🌤️ 예상 날씨",
        ["☀️ 맑음", "⛅ 흐림", "🌧️ 비", "❄️ 눈"]
    )
    # 날씨에서 이모지 제거하여 저장
    weather_clean = weather.split(" ")[1]

    num_people = st.number_input(
        "👥 탑승 인원",
        min_value=1,
        max_value=100,
        value=1,
        help="함께 여행할 인원 수는?"
    )

    budget = st.number_input(
        "💰 예산",
        min_value=0,
        value=0,
        step=10000,
        help="여행에 쓸 수 있는 예산을 입력하세요 (0원 = 예산 없음)"
    )

    st.markdown("---")
    st.info("🎒 가방은 챙기셨나요?")

# 모드 선택 (첫 시작 또는 모드 변경 시)
if st.session_state.mode is None:
    st.markdown("")
    st.markdown("")
    st.markdown('<div class="section-title">🎯 여행 계획 모드를 선택하세요</div>', unsafe_allow_html=True)
    st.markdown("")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🎮 사용자 참여 모드\n(AI와 함께 대화하며 만들기)",
            use_container_width=True,
            key="btn_user_mode",
            help="AI가 선택지를 제공하고, 당신이 선택합니다"
        ):
            st.session_state.mode = "user"
            st.session_state.current_step = 0
            st.rerun()

    with col2:
        if st.button(
            "⚡ AI 자동 모드\n(빠르게 생성)",
            use_container_width=True,
            key="btn_ai_mode",
            help="AI가 자동으로 완벽한 일정을 만들어줍니다"
        ):
            st.session_state.mode = "ai"
            st.session_state.current_step = 0
            st.rerun()

# 모드 변경 버튼 (모드가 선택된 후)
if st.session_state.mode is not None:
    st.markdown("")
    if st.button("🔄 모드 변경", use_container_width=False, key="change_mode"):
        # 모든 세션 상태 초기화
        st.session_state.mode = None
        st.session_state.current_step = 0
        st.session_state.selected_style = None
        st.session_state.first_place = None
        st.session_state.final_itinerary = None
        st.session_state.final_cost = None
        st.rerun()

# AI 자동 모드
if st.session_state.mode == "ai":
    st.markdown("")
    st.markdown("")
    if not city:
        st.error("❌ 도시 이름을 입력해주세요!")
    else:
        # 여행 코스 생성
        prompt = f"""{city} {weather_clean} 날씨 하루 여행 일정

이 일정에 포함시킬 것:
- 유명한 곳뿐 아니라 현지인들이 가는 숨은 곳들
- 음식, 자연, 문화, 쇼핑, 예술 등 다양한 경험
- 매번 다른 구성의 여행

형식:
1. [장소명]
   시간: [시작~끝 시간]
   소요시간: [시간]
   특징: [설명]

2. [장소명]
   ...
"""

        # 비용 계산
        cost_prompt = f"""{city} {weather_clean} 날씨 하루 여행 비용 ({num_people}명)

현실적인 평균 가격으로 계산:

## 이동 비용
- 설명:
- 1인당: 원
- {num_people}명: 원

## 음식
- 아침: 원
- 점심: 원
- 저녁: 원
- 1인당 합계: 원
- {num_people}명 합계: 원

## 입장료/액티비티
- 무료 명소 중심: 원
- 주요 관광지: 원

## 기타
- 간식/기념품: 원

## 총 예산

**최저 예산**
1인당: 원
{num_people}명: 원

**중간 예산**
1인당: 원
{num_people}명: 원

**넉넉한 예산**
1인당: 원
{num_people}명: 원
"""

        # 진행 상황 표시
        with st.spinner("여행 일정을 정리 중..."):
            itinerary = ask_ai(prompt)

        with st.spinner("비용을 계산 중..."):
            cost_estimate = ask_ai(cost_prompt)

        # 성공 메시지
        st.markdown("")
        st.success("🛫 설렘 가득한 여행 계획이 준비되었습니다! 가보시겠어요?")
        st.markdown("")

        # 여행 코스 표시
        st.markdown('<div class="section-title">🗺️ 일정표</div>', unsafe_allow_html=True)
        st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
        st.markdown(itinerary)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("")

        # 비용 정보 표시
        st.markdown('<div class="section-title">💳 여행 경비</div>', unsafe_allow_html=True)
        st.markdown(cost_estimate)

        # 예산 비교 (예산이 입력된 경우)
        if budget > 0:
            st.markdown("")
            st.markdown('<div class="section-title">💼 예산 확인</div>', unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("💰 내 예산", f"{budget:,}원")
            with col2:
                st.metric("💳 권장 비용", f"{int(budget * 0.8):,}원")
            with col3:
                remaining = budget - int(budget * 0.8)
                if remaining >= 0:
                    st.metric("✅ 여유 금액", f"{remaining:,}원")
                else:
                    st.metric("⚠️ 부족 금액", f"{abs(remaining):,}원")

            st.markdown("")
            if remaining >= 0:
                st.success(f"✨ 좋은 소식! 예산이 충분합니다. 여유 있게 여행을 즐기세요!")
            else:
                st.warning(f"💡 예산이 약간 부족하네요. 무료 명소 중심으로 계획하면 좋습니다!")

        st.markdown("")
        st.markdown("")

        # 여행 정보 요약
        st.markdown("### 🎫 탑승 정보")
        st.markdown("")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏖️ 목적지", city)
        with col2:
            st.metric("🌤️ 날씨", weather_clean)
        with col3:
            st.metric("👥 인원", f"{num_people}명")


# 사용자 참여 모드
elif st.session_state.mode == "user":
    st.markdown("")
    st.markdown("")
    st.markdown('<div class="section-title">🎮 함께 만드는 여행 계획</div>', unsafe_allow_html=True)

    if st.session_state.current_step == 0:
        st.markdown("")
        st.markdown('<h3 style="font-size: 1.8em; color: #c0c0c0; margin: 20px 0;">📋 1단계: 여행 스타일을 선택해주세요</h3>', unsafe_allow_html=True)
        st.markdown("")

        # 여행 스타일 선택
        style_prompt = f"""{city} {weather_clean} 날씨에 어울리는 여행 스타일 4가지

1. [스타일]: [설명]
2. [스타일]: [설명]
3. [스타일]: [설명]
4. [스타일]: [설명]

각각 다른 특징의 여행을 제시해."""

        styles = ask_ai(style_prompt).split('\n')
        styles = [s for s in styles if s.strip() and s[0].isdigit()]

        for idx, style in enumerate(styles[:4]):
            if st.button(style, use_container_width=True, key=f"style_btn_{idx}"):
                st.session_state.selected_style = style
                st.session_state.current_step = 1
                st.rerun()

    elif st.session_state.current_step == 1:
        st.markdown("")
        st.markdown(f'<div style="background: #1f2937; padding: 15px; border-radius: 10px; border-left: 4px solid #00d4ff; margin: 15px 0;"><h3 style="color: #00d4ff; margin: 0; font-size: 1.2em;">✅ 선택한 스타일</h3><p style="color: #e8e8e8; margin: 10px 0 0 0; font-size: 1.1em;">{st.session_state.selected_style}</p></div>', unsafe_allow_html=True)
        st.markdown("")
        st.markdown('<h3 style="font-size: 1.8em; color: #c0c0c0; margin: 20px 0;">🏝️ 2단계: 먼저 어디서 시작할까요?</h3>', unsafe_allow_html=True)
        st.markdown("")

        # 첫 목적지 선택
        first_prompt = f"""{city} {st.session_state.selected_style} 여행 시작점 4곳

1. [장소]: [설명]
2. [장소]: [설명]
3. [장소]: [설명]
4. [장소]: [설명]

서로 다른 위치와 특징의 장소를 제시해."""

        first_places = ask_ai(first_prompt).split('\n')
        first_places = [p for p in first_places if p.strip() and p[0].isdigit()]

        for idx, place in enumerate(first_places[:4]):
            if st.button(place, use_container_width=True, key=f"place_btn_{idx}"):
                st.session_state.first_place = place
                st.session_state.current_step = 2
                st.rerun()

    elif st.session_state.current_step == 2:
        st.markdown("")
        st.markdown(f'<div style="background: #1f2937; padding: 15px; border-radius: 10px; border-left: 4px solid #00d4ff; margin: 15px 0;"><h3 style="color: #00d4ff; margin: 0; font-size: 1.2em;">✅ 첫 목적지</h3><p style="color: #e8e8e8; margin: 10px 0 0 0; font-size: 1.1em;">{st.session_state.first_place}</p></div>', unsafe_allow_html=True)
        st.markdown("")
        st.markdown('<h3 style="font-size: 1.8em; color: #c0c0c0; margin: 20px 0;">✨ 3단계: 전체 일정을 만들어드릴까요?</h3>', unsafe_allow_html=True)
        st.markdown("")

        if st.button("✨ 완벽한 일정 만들기", use_container_width=True, key="create_itinerary"):
            with st.spinner("당신의 여행 일정을 만들고 있습니다..."):
                itinerary_prompt = f"""{city} {weather_clean} {st.session_state.selected_style} 여행
시작점: {st.session_state.first_place}

하루 일정:

1. [장소]
   시간: [시작~끝]
   소요: [시간]
   특징: [설명]

2. [장소]
   ...
"""

                itinerary = ask_ai(itinerary_prompt)

            with st.spinner("여행 비용을 계산하고 있습니다..."):
                cost_prompt = f"""{city} {st.session_state.selected_style} 여행 비용 ({num_people}명)
날씨: {weather_clean}

현실적 평균 가격:

## 이동
[설명]
1인당: 원
{num_people}명: 원

## 음식
아침: 원
점심: 원
저녁: 원
1인당: 원
{num_people}명: 원

## 입장료/액티비티
최저: 원
중간: 원

## 기타
간식/기념품: 원

## 총액

최저 예산 - 1인: 원, {num_people}명: 원
중간 예산 - 1인: 원, {num_people}명: 원
넉넉함 - 1인: 원, {num_people}명: 원
"""

                cost_estimate = ask_ai(cost_prompt)

            st.session_state.final_itinerary = itinerary
            st.session_state.final_cost = cost_estimate
            st.session_state.current_step = 3
            st.rerun()

    elif st.session_state.current_step == 3:
        st.markdown("")
        st.success("🛫 당신을 위해 특별히 만들어진 여행 계획이 준비되었습니다!")
        st.markdown("")

        st.markdown('<div class="section-title">🗺️ 일정표</div>', unsafe_allow_html=True)
        st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
        st.markdown(st.session_state.final_itinerary)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("")

        st.markdown('<div class="section-title">💳 여행 경비</div>', unsafe_allow_html=True)
        st.markdown(st.session_state.final_cost)

        # 예산 비교 (예산이 입력된 경우)
        if budget > 0:
            st.markdown("")
            st.markdown('<div class="section-title">💼 예산 확인</div>', unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("💰 내 예산", f"{budget:,}원")
            with col2:
                st.metric("💳 권장 비용", f"{int(budget * 0.8):,}원")
            with col3:
                remaining = budget - int(budget * 0.8)
                if remaining >= 0:
                    st.metric("✅ 여유 금액", f"{remaining:,}원")
                else:
                    st.metric("⚠️ 부족 금액", f"{abs(remaining):,}원")

            st.markdown("")
            if remaining >= 0:
                st.success(f"✨ 좋은 소식! 예산이 충분합니다. 여유 있게 여행을 즐기세요!")
            else:
                st.warning(f"💡 예산이 약간 부족하네요. 무료 명소 중심으로 계획하면 좋습니다!")

        st.markdown("")
        st.markdown("")
        st.markdown("### 🎫 탑승 정보")
        st.markdown("")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏖️ 목적지", city)
        with col2:
            st.metric("🌤️ 날씨", weather_clean)
        with col3:
            st.metric("👥 인원", f"{num_people}명")
