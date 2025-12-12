import streamlit as st

# 1. 게임 제목 및 설정
st.set_page_config(page_title="대저택 탈출", page_icon="🗝️")
st.title('🏰 대저택 탈출: 수학자의 유산')

# 2. 게임 상태 초기화
if 'current_room' not in st.session_state:
    st.session_state.current_room = 1  # 1: 서재, 2: 유리방, 3: 대도서관
if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'log' not in st.session_state:
    # 최신 로그가 맨 위에 오도록 하기 위해 초기 메시지를 리스트에 담음
    st.session_state.log = [] 
    
# 방 별 클리어 여부
if 'room1_cleared' not in st.session_state:
    st.session_state.room1_cleared = False
if 'room2_cleared' not in st.session_state:
    st.session_state.room2_cleared = False
if 'game_cleared' not in st.session_state:
    st.session_state.game_cleared = False

# 3. 핵심 함수들

# 로그 추가 함수 (수정됨: 최신 글이 리스트의 맨 앞(0번)으로 옴)
def add_log(message):
    st.session_state.log.insert(0, message)

# --- 1단계: 수학자의 서재 함수 ---
def room1_check_clock():
    add_log('>> [벽시계] 멈춰있습니다. 시침: 9시, 분침: 15분')

def room1_check_calendar():
    add_log('>> [달력] 10월 3일 개천절에 빨간 동그라미가 있습니다.')

def room1_check_note():
    add_log('>> [쪽지] "비밀번호 = (월 + 일) - 시계의 분"')

def room1_try_door(password):
    # 정답: (10 + 3) - 15 = -2 (음수가 나올 수 있음!)
    if password == '-2' or password == '-02':
        add_log('✅ 정답! 서재 문이 열리고 다음 방으로 이동합니다.')
        st.session_state.room1_cleared = True
        st.session_state.current_room = 2 # 2번 방으로 이동
        add_log('--- [2단계: 유리 정원]에 진입했습니다. ---')
    else:
        add_log('❌ 틀렸습니다. (힌트: 결과가 음수일 수도 있습니다)')

# --- 2단계: 유리 정원 함수 (빛과 반사) ---
def room2_desc():
    st.info("사방이 유리로 된 방입니다. 빛이 여러 갈래로 굴절되고 있습니다.")

def room2_inspect_prism():
    add_log('>> [프리즘] 햇빛이 프리즘을 통과해 3가지 색(빨강, 초록, 파랑)으로 나뉩니다.')

def room2_inspect_mirror():
    add_log('>> [거울] 거울 구석에 작게 숫자가 적혀 있습니다. "Red=5, Green=2, Blue=9"')

def room2_inspect_floor():
    add_log('>> [바닥] 유리에 글귀가 새겨져 있습니다. "가장 강한 빛부터 약한 빛 순서로..."')
    add_log('>> (추가 단서: 빛의 파장은 빨강 > 초록 > 파랑 순서로 깁니다.)')

def room2_try_door(password):
    # 정답: 빨(5) -> 초(2) -> 파(9) => 529
    if password == '529':
        add_log('✅ 쨍그랑! 유리문이 열렸습니다.')
        st.session_state.room2_cleared = True
        st.session_state.current_room = 3 # 3번 방으로 이동
        add_log('--- [3단계: 대도서관]에 진입했습니다. ---')
    else:
        add_log('❌ 유리에 비친 내 모습이 고개를 젓습니다.')

# --- 3단계: 대도서관 함수 (책 조합) ---
def room3_desc():
    st.info("수천 권의 책이 꽂힌 거대한 서재입니다. 책들은 3가지 색상으로 분류되어 있습니다.")

def room3_search_red():
    add_log('>> [빨간 책장] "전쟁과 평화" 1권을 찾았습니다. (책등 번호: 100)')

def room3_search_blue():
    add_log('>> [파란 책장] "바다의 역사" 2권을 찾았습니다. (책등 번호: 50)')

def room3_search_yellow():
    add_log('>> [노란 책장] "황금의 제국" 3권을 찾았습니다. (책등 번호: 10)')

def room3_read_guide():
    add_log('>> [사서의 메모] "진리는 빨간색에서 시작해 파란색을 더하고, 노란색으로 나누어 완성된다."')

def room3_try_final(password):
    # 정답: (빨강 100 + 파랑 50) / 노랑 10 = 15
    if password == '15':
        add_log('🎉 축하합니다! 마지막 문이 열리고 바깥 세상의 빛이 들어옵니다!')
        add_log('🏆 대저택 탈출 성공!')
        st.session_state.game_cleared = True
    else:
        add_log('❌ 굳게 닫힌 문은 꿈쩍도 하지 않습니다.')

# 초기화 함수
def restart_game():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

# 4. 화면 구성 (UI)

# (1) 로그창 (가장 중요한 변경점: 최신 글이 위로 오도록 함)
st.subheader('📜 행동 기록 (최신순)')
# 로그 리스트를 줄바꿈으로 합쳐서 보여줌
log_text = '\n\n'.join(st.session_state.log)
# 높이를 넉넉하게 300으로 줌
st.text_area("Log", log_text, height=300, disabled=True)

st.divider()

# (2) 게임 클리어 화면
if st.session_state.game_cleared:
    st.balloons()
    st.success("🏆 모든 방을 탈출하셨습니다! 당신은 천재인가요?")
    if st.button("처음부터 다시 하기"):
        restart_game()

# (3) 방 별 컨트롤 패널
else:
    # === 1번방: 수학자의 서재 ===
    if st.session_state.current_room == 1:
        st.markdown("### 1단계: 수학자의 서재")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🕰️ 시계 확인"): room1_check_clock(); st.rerun()
            if st.button("📅 달력 확인"): room1_check_calendar(); st.rerun()
        with col2:
            if st.button("📝 쪽지 확인"): room1_check_note(); st.rerun()
            with st.popover("🔐 방문 열기"):
                pw = st.text_input("비밀번호 입력")
                if st.button("확인"): room1_try_door(pw); st.rerun()

    # === 2번방: 유리 정원 ===
    elif st.session_state.current_room == 2:
        st.markdown("### 2단계: 유리 정원")
        room2_desc()
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💎 프리즘 조사"): room2_inspect_prism(); st.rerun()
        with col2:
            if st.button("🪞 거울 조사"): room2_inspect_mirror(); st.rerun()
        with col3:
            if st.button("🔍 바닥 조사"): room2_inspect_floor(); st.rerun()
        
        st.write("") # 여백
        with st.popover("🔐 유리문 열기"):
            pw = st.text_input("숫자 코드 입력")
            if st.button("도전"): room2_try_door(pw); st.rerun()

    # === 3번방: 대도서관 ===
    elif st.session_state.current_room == 3:
        st.markdown("### 3단계: 대도서관")
        room3_desc()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📕 빨간 책장"): room3_search_red(); st.rerun()
            if st.button("📘 파란 책장"): room3_search_blue(); st.rerun()
        with col2:
            if st.button("📒 노란 책장"): room3_search_yellow(); st.rerun()
            if st.button("📜 사서의 메모"): room3_read_guide(); st.rerun()
        
        st.write("---")
        st.warning("마지막 관문입니다. 신중하게 답을 입력하세요.")
        input_col, btn_col = st.columns([3, 1])
        with input_col:
            final_pw = st.text_input("최종 비밀번호", key="final_pw")
        with btn_col:
            st.write("") # 줄맞춤용
            st.write("") 
            if st.button("탈출!"):
                room3_try_final(final_pw)
                st.rerun()