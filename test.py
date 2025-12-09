import streamlit as st

# 1. 게임 제목
st.title('🔒 방탈출 게임: 어두운 독방')

# 2. 게임 상태 초기화 (새로고침 해도 데이터 유지)
if 'inventory' not in st.session_state:
    st.session_state.inventory = [] 
if 'key_found' not in st.session_state:
    st.session_state.key_found = False
if 'game_cleared' not in st.session_state:
    st.session_state.game_cleared = False
if 'log' not in st.session_state:
    st.session_state.log = ['당신은 차가운 방 바닥에서 눈을 떴습니다.', '주변에는 [침대]와 굳게 닫힌 [문]이 보입니다.']

# 3. 기능 함수들
def add_log(message):
    st.session_state.log.append(message)

def check_bed():
    if st.session_state.key_found:
        add_log('>> 이미 침대 밑을 확인했습니다. 먼지뿐입니다.')
    else:
        add_log('>> 침대 베개를 들추자 [황금 열쇠]가 나왔습니다!')
        add_log('>> [황금 열쇠]를 가방에 넣었습니다.')
        st.session_state.inventory.append('황금 열쇠')
        st.session_state.key_found = True

def open_door():
    if '황금 열쇠' in st.session_state.inventory:
        add_log('>> 찰칵! 열쇠가 구멍에 딱 맞습니다.')
        add_log('>> 끼익... 문이 열렸습니다. 탈출 성공! 🎉')
        st.session_state.game_cleared = True
    else:
        add_log('>> 문은 잠겨 있습니다. 열쇠가 필요해 보입니다.')

def restart():
    st.session_state.inventory = []
    st.session_state.key_found = False
    st.session_state.game_cleared = False
    st.session_state.log = ['게임을 다시 시작합니다.', '주변에는 [침대]와 굳게 닫힌 [문]이 보입니다.']

# 4. 화면 표시 (UI)
st.subheader('게임 상황')
# 로그가 너무 길어지면 최근 5줄만 보여주기
for msg in st.session_state.log[-5:]:
    st.text(msg)

st.write('---')

if st.session_state.game_cleared:
    st.success('축하합니다! 방을 탈출했습니다.')
    if st.button('다시 하기'):
        restart()
        st.rerun()
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('침대 조사'):
            check_bed()
            st.rerun()
    with col2:
        if st.button('문 열기'):
            open_door()
            st.rerun()
    with col3:
        if st.button('가방 확인'):
            st.info(f'소지품: {st.session_state.inventory}')