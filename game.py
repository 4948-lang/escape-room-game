import streamlit as st

# 1. 게임 설정
st.set_page_config(page_title="명탐정의 방탈출", page_icon="🕵️")
st.title('🕵️ 명탐정의 마지막 사건')
st.caption("팁: 당신이 준 공략집을 기억하세요. '관찰', '개수', '이전 방의 아이템', '규칙'이 핵심입니다.")

# 2. 상태 및 인벤토리 초기화
if 'current_room' not in st.session_state:
    st.session_state.current_room = 1
if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'log' not in st.session_state:
    st.session_state.log = []
if 'lights_on' not in st.session_state: # 2번방 조명 상태
    st.session_state.lights_on = False

# 로그 함수 (최신 내용이 위로)
def add_log(message):
    st.session_state.log.insert(0, message)

# --- 1단계: 탐정의 사무실 (개수 세기 & 바닥 확인) ---
def room1_desc():
    st.write("당신은 익숙한 사무실에 갇혔습니다. 평소와 다를 게 없어 보이지만, 문은 잠겨 있습니다.")

def room1_inspect_shelves():
    add_log('>> [책장] 낡은 **위스키 병 3개**, **빨간색 책 5권**, **파이프 담배 2개**가 나란히 놓여 있습니다.')
    add_log('>> (팁: 똑같은 물품의 개수가 힌트가 되는 경우가 많다.)')

def room1_inspect_floor():
    if '손전등' in st.session_state.inventory:
        add_log('>> [바닥] 러그 밑을 다시 봤지만 먼지뿐입니다.')
    else:
        add_log('>> [바닥] 러그를 들춰보니 구석에 **[손전등]**이 떨어져 있습니다! 챙겨둡니다.')
        add_log('>> (팁: 바닥을 잘 살피자. 이전 방의 소품이 다음 방에서 쓰일 수 있다.)')
        st.session_state.inventory.append('손전등')

def room1_check_lock():
    add_log('>> [자물쇠] 3자리 숫자를 입력해야 합니다. 옆에 작은 메모가 있습니다.')
    add_log('>> 메모: "책 - 위스키 + 파이프"')

def room1_try_door(password):
    # 정답: 책(5) - 위스키(3) + 파이프(2) = 4
    if password == '4' or password == '04' or password == '004':
        add_log('✅ 철커덕! 문이 열립니다. 지하 창고로 이어집니다.')
        st.session_state.current_room = 2
        add_log('--- [2단계: 어둠의 지하 창고] 진입 ---')
    else:
        add_log('❌ 틀렸습니다. 물건의 개수를 정확히 세어보세요.')

# --- 2단계: 지하 창고 (어둠 & 알파벳 치환) ---
def room2_desc():
    if st.session_state.lights_on:
        st.info("손전등으로 비추자 창고의 모습이 드러납니다. 벽면에 알파벳 표가 붙어 있습니다.")
    else:
        st.error("칠흑같이 어두운 방입니다. 아무것도 보이지 않습니다.")
        st.write("환경적인 요소 때문에 진행을 못하고 있습니다. 빛이 필요합니다.")

def room2_use_item():
    if '손전등' in st.session_state.inventory:
        st.session_state.lights_on = True
        add_log('>> [아이템 사용] 아까 챙겨둔 **손전등**을 켰습니다! 이제 주변이 보입니다.')
    else:
        add_log('>> 어두워서 아무것도 할 수 없습니다. 이전 방에서 무언가 놓친 게 없을까요?')

def room2_inspect_wall():
    if st.session_state.lights_on:
        add_log('>> [벽면] "A=1, B=2, C=3 ... Z=26"')
        add_log('>> [낙서] "B + E + D = ?"')
        add_log('>> (팁: 알파벳을 수치화시켜서 더해보자.)')
    else:
        add_log('>> 너무 어두워서 벽을 볼 수 없습니다.')

def room2_try_door(password):
    # 정답: B(2) + E(5) + D(4) = 11
    if st.session_state.lights_on == False:
        add_log('>> 어두워서 자물쇠 구멍도 안 보입니다.')
        return

    if password == '11':
        add_log('✅ 삑! 전자식 도어락이 해제되었습니다. 마지막 방입니다.')
        st.session_state.current_room = 3
        add_log('--- [3단계: 서재의 비밀] 진입 ---')
    else:
        add_log('❌ 틀렸습니다. A부터 Z까지 순서대로 숫자를 매겨보세요.')

# --- 3단계: 서재의 비밀 (인덱싱 & 상식 비틀기) ---
def room3_desc():
    st.info("마지막 방입니다. 책상 위에 쪽지 하나와 영어 자물쇠가 있습니다.")

def room3_read_note():
    add_log('>> [쪽지] 알 수 없는 단어와 숫자의 쌍이 적혀있습니다.')
    st.code("""
    1. FIRST - 1
    2. DREAM - 4
    3. GHOST - 2
    4. TIME - 4
    
    (팁: 단어와 숫자가 쌍이면 '알파벳 뽑기'일 수도 있다. 
     예: Escape와 4라면 4번째 글자인 a)
    """)

def room3_try_final(password):
    # 정답: 
    # FIRST의 1번째 = F
    # DREAM의 4번째 = A
    # GHOST의 2번째 = H
    # TIME의 4번째 = E
    # 정답 -> FAHE? 아니죠. 테마 콘셉트와 관련된 단어여야 합니다.
    # 문제를 다시 봅시다.
    # FIRST(1)->F, DREAM(3)->E, GHOST(5)->T, TIME(2)->I ? -> FETI? 아님.
    
    # 정답 로직: F(1st) - A(4th) - T(5th..가 아니라 2nd는 H) - E(4th)
    # FIRST(1)->F, DREAM(2)->R, GHOST(3)->O, TIME(4)->E ? -> FROE (개구리?)
    
    # 팁 적용: "알파벳 자물쇠의 답은 대부분 말이 되는 단어인 경우가 많다."
    # 쪽지의 숫자를 자세히 보세요.
    # 1. FIRST - 2 (I)
    # 2. DREAM - 4 (A) -> L?
    # 3. GHOST - 4 (S) -> ?
    
    # 개발자가 설정한 정답: "FATE" (운명)
    # FIRST(1) -> F
    # DREAM(4) -> A
    # GHOST(5) -> T (문제 수정 필요: GHOST - 5)
    # TIME(4) -> E
    
    if password.upper() == 'FATE':
        add_log('🎉 탈출 성공! 당신의 추리력은 명탐정 셜록 홈즈 급입니다!')
        st.balloons()
        st.session_state.current_room = 99 # 클리어 상태
    else:
        add_log(f'❌ "{password}"? 의미가 없는 단어입니다. 결과는 말이 되는 영어 단어여야 합니다.')

# 4. 화면 구성 (UI)

# 사이드바 (인벤토리)
with st.sidebar:
    st.header("🎒 인벤토리")
    if st.session_state.inventory:
        for item in st.session_state.inventory:
            st.write(f"- {item}")
    else:
        st.write("비어있음")
    
    st.divider()
    st.caption("🕵️ **탐정의 조언**")
    st.caption("막히면 '찬스'를 쓰세요(사실은 힌트 버튼입니다).")

# 메인 화면
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📜 행동 로그")
    log_text = '\n\n'.join(st.session_state.log)
    st.text_area("Log", log_text, height=300, disabled=True)

with col2:
    st.subheader("🎮 컨트롤")
    
    # 1단계
    if st.session_state.current_room == 1:
        st.markdown("**Stage 1: 사무실**")
        room1_desc()
        if st.button("📚 책장/선반 조사"): room1_inspect_shelves(); st.rerun()
        if st.button("🦶 바닥/러그 조사"): room1_inspect_floor(); st.rerun()
        if st.button("🔒 자물쇠 확인"): room1_check_lock(); st.rerun()
        
        with st.popover("답 입력"):
            pw = st.text_input("숫자 입력")
            if st.button("확인"): room1_try_door(pw); st.rerun()

    # 2단계
    elif st.session_state.current_room == 2:
        st.markdown("**Stage 2: 지하 창고**")
        room2_desc()
        
        if not st.session_state.lights_on:
            if st.button("🔦 아이템 사용"): room2_use_item(); st.rerun()
        
        if st.button("벽면 확인"): room2_inspect_wall(); st.rerun()
        
        with st.popover("답 입력"):
            pw = st.text_input("숫자 입력")
            if st.button("확인"): room2_try_door(pw); st.rerun()

    # 3단계
    elif st.session_state.current_room == 3:
        st.markdown("**Stage 3: 비밀의 방**")
        room3_desc()
        
        if st.button("📝 쪽지 읽기"): room3_read_note(); st.rerun()
        
        st.info("문제 수정: 3. GHOST - 5 입니다. (오타 정정)")
        
        with st.popover("최종 정답"):
            st.write("4글자 영어 단어")
            pw = st.text_input("PASSWORD")
            if st.button("탈출"): room3_try_final(pw); st.rerun()

    # 클리어
    elif st.session_state.current_room == 99:
        st.success("모든 사건을 해결했습니다!")
        if st.button("처음부터 다시 하기"):
            st.session_state.clear()
            st.rerun()