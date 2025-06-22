import streamlit as st
import openai
import requests
from PIL import Image
from io import BytesIO

# import os
# from dotenv import load_dotenv
# load_dotenv()

# openai_api_key = os.environ.get("OPENAI_API_KEY")

# OpenAI API 키 설정
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="대학생 GPT 학습 도우미", layout="wide")
st.title("🎓 대학생 GPT 학습 도우미")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 파일 업로드
uploaded_file = st.file_uploader("이미지 업로드 (선택)", type=["png", "jpg", "jpeg"])

# 사용자 입력
user_input = st.text_area("질문을 입력하세요:", height=100)
submit = st.button("질문하기")

if submit and user_input:
    with st.spinner("GPT에게 질문 중..."):
        user_message = {"role": "user", "content": []}

        # 텍스트 추가
        user_message["content"].append({"type": "text", "text": user_input})

        # 이미지 업로드 시 base64로 전송
        if uploaded_file:
            image_bytes = uploaded_file.read()
            image_url = st.secrets.get("TEMP_IMAGE_HOSTING_URL")  # 이미지 호스팅 서버 (예: S3, Cloudflare)
            if image_url:
                # 간단한 예시: 이미지 호스팅 서버 없이 로컬 프리뷰
                image = Image.open(BytesIO(image_bytes))
                st.image(image, caption="업로드한 이미지", use_column_width=True)
                user_message["content"].append({
                    "type": "image_url",
                    "image_url": {"url": image_url}  # 실제 URL로 교체 필요
                })

        # GPT-4-Vision API 호출
        response = openai.chat.completions.create(
            model="gpt-4-vision-preview" if uploaded_file else "gpt-4-turbo",
            messages=[user_message],
            max_tokens=1000
        )

        # 응답 처리
        assistant_reply = response.choices[0].message.content
        st.session_state.messages.append((user_input, assistant_reply))

# 이전 대화 표시
if st.session_state.messages:
    st.subheader("💬 대화 기록")
    for i, (q, a) in enumerate(reversed(st.session_state.messages)):
        st.markdown(f"**Q{i+1}:** {q}")
        st.markdown(f"**A{i+1}:** {a}")




import requests

st.title("📡 Django 서버에서 데이터 가져오기")

# 사용자가 버튼을 누르면 GET 요청
if st.button("서버에 요청 보내기"):
    try:
        response = requests.get("https://8000-animated-bassoon-wqwq77p77xw25qx4.app.github.dev/main/api/text/")  # 로컬에서 Django 서버가 실행 중이어야 함
        response.raise_for_status()
        data = response.json()
        st.success(f"✅ 서버 응답: {data}")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ 요청 에러: {e}")
    except ValueError:
        st.error("❌ JSON 파싱 에러: 서버가 JSON 형식이 아닌 응답을 보냈어요.")