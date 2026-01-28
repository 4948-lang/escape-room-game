import streamlit as st

# 1. 게임 설정
st.set_page_config(page_title="미식가의 방탈출", page_icon="🥢")
st.title('🥢 방탈출: 통영의 미식가')
st.caption("텍스트 속에 숨겨진 '숫자'를 찾으세요. 순서가 중요합니다.")

# 2. 상태 초기화
if 'stage' not in st.session_state:
    st.session_state.stage = 1
if 'log' not in st.session_state:
    st.session_state.log = []

# 로그 함수
def add_log(message):
    st.session_state.log.insert(0, message)

# --- 시나리오 텍스트 (제공해주신 내용) ---
story_text = """
"나의 돈키호테 184p."
"""

# --- 기능 함수 ---
def inspect_receipt():
    add_log(">> '코스는 총 4번.'")
    add_log(">> [영수증] 가격 대신 이상한 문구가 적혀 있습니다.")

def inspect_photo():
    add_log(">> 접시 위에 가득 찬 해산물들이 보입니다. (텍스트를 꼼꼼히 읽어보세요.)")

def try_unlock(password):
    # 정답: 2(옥수수,홍합) - 1(굴) - 8(해물모둠) - 4(회3+국1)
    if password == '2184':
        st.balloons()
        st.success("🎉 정답! 배부르게 먹고 탈출에 성공했습니다!")
        st.session_state.stage = 99 # 클리어
    else:
        add_log(f"❌ '{password}'? 틀렸습니다.")
        add_log(">> 힌트: 생굴은 모둠 접시에 없었습니다. 먼저 나왔죠.")

# --- UI 구성 ---

# 1. 스토리 보여주기
st.markdown("### 📜 오늘의 일기")
st.info(story_text) # 텍스트 박스로 강조

# 2. 로그창
st.subheader("행동 기록")
log_text = '\n\n'.join(st.session_state.log)
st.text_area("Log", log_text, height=200, disabled=True)

# 3. 컨트롤 패널
st.divider()

if st.session_state.stage == 99:
    if st.button("다시 하기"):
        st.session_state.stage = 1
        st.session_state.log = []
        st.rerun()
else:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧾 영수증 확인"): inspect_receipt(); st.rerun()
    with col2:
        if st.button("📱 친구 폰 확인"): inspect_photo(); st.rerun()
    
    st.write("")
    st.warning("문이 잠겨있습니다. 비밀번호 4자리는?")
    
    with st.popover("비밀번호 입력"):
        pw = st.text_input("숫자 4자리")
        if st.button("입력"): try_unlock(pw); st.rerun()