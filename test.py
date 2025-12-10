import streamlit as st

# 1. 게임 제목
st.title('🕵️ 방탈출: 수학자의 서재')

# 2. 게임 상태 초기화
if 'inventory' not in st.session_state:
    st.session_state.inventory = [] 
if 'safe_opened' not in st.session_state:
    st.session_state.safe_opened = False
if 'game_cleared' not in st.session_state:
    st.session_state.game_cleared = False
if 'log' not in st.session_state:
    st.session_state.log = ['당신은 어느 수학자의 서재에 갇혔습니다.', '단서를 모아 금고를 열어야 합니다.']

# 3. 기능 함수들 (여기가 핵심!)
def add_log(message):
    st.session_state.log.append(message)

def check_clock():
    add_log('>> [벽시계]를 봅니다. 낡아서 멈춰있습니다.')
    add_log('>> 시침은 10시, 분침은 30분을 가리킵니다.')

def check_calendar():
    add_log('>> [달력]을 봅니다. 12월 달력입니다.')
    add_log('>> 날짜 25일에 빨간 동그라미가 쳐져 있습니다.')

def check_note():
    add_log('>> 바닥에 떨어진 [쪽지]를 주웠습니다.')
    add_log('>> 힌트: "비밀번호 = (달력의 월 + 달력의 일) - 시계의 시"')

def try_safe(password):
    if st.session_state.safe_opened:
        add_log('>> 금고는 이미 열려있습니다.')
    # 정답: (12 + 25) - 10 = 27
    elif password == '27': 
        add_log('>> 띠리릭! 정답입니다!')
        add_log('>> 금고 안에서 [도서관 열쇠]를 발견했습니다.')
        st.session_state.inventory.append('도서관 열쇠')
        st.session_state.safe_opened = True
    else:
        add_log('>> 비밀번호가 틀렸습니다. 다시 계산해보세요.')

def open_door():
    if '도서관 열쇠' in st.session_state.inventory:
        add_log('>> 찰칵! 문이 열렸습니다. 탈출 성공! 🎉')
        st.session_state.game_cleared = True
    else:
        add_log('>> 문은 잠겨 있습니다. 열쇠가 필요합니다.')

def restart():
    st.session_state.inventory = []
    st.session_state.safe_opened = False
    st.session_state.game_cleared = False
    st.session_state.log = ['게임을 다시 시작합니다.']

# 4. 화면 표시 (UI)
st.subheader('📜 게임 로그')
log_text = '\n'.join(st.session_state.log)
st.text_area("기록", log_text, height=200)

st.write('---')

if st.session_state.game_cleared:
    st.success('축하합니다! 방을 탈출했습니다.')
    if st.button('다시 하기'):
        restart()
        st.rerun()
else:
    # 버튼 4개를 2줄로 배치 (col1, col2)
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button('🕰️ 시계 확인'):
            check_clock()
            st.rerun()
        if st.button('📅 달력 확인'):
            check_calendar()
            st.rerun()
            
    with col2:
        if st.button('📄 쪽지 읽기'):
            check_note()
            st.rerun()
        # 금고 버튼 (팝오버)
        with st.popover("🔐 금고 열기"):
            st.write("힌트를 조합해 숫자를 입력하세요.")
            user_pass = st.text_input("Password")
            if st.button("입력"):
                try_safe(user_pass)
                st.rerun()

    st.write('---')
    if st.button('🚪 문 열기'):
        open_door()
        st.rerun()

    st.info(f'🎒 소지품: {st.session_state.inventory}')