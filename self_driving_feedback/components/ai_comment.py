# components/ai_comment.py

import openai
import os
from dotenv import load_dotenv
from components.prompt_generator import generate_prompt

# .env 파일 로드 및 OpenAI API Key 설정
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def call_openai(prompt: str) -> str:
    """
    OpenAI Chat API (1.0.0 이상) 사용 예시.
    'openai.ChatCompletion.create' 대신
    'openai.chat.completions.create' 형태를 사용합니다.
    """
    try:
        # 새로운 ChatCompletion 인터페이스
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "너는 감성적인 자율 주행 리뷰어이다."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.85,
            max_tokens=1000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f'{{"error": "OpenAI API 호출 오류: {e}"}}'
