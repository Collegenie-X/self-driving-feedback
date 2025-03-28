def generate_prompt(analysis_stats):
    prompt = f"""
너는 자율 주행 시스템에 대한 감성적인 리뷰어이다.
다음 평균 점수를 참고하여, 각 항목에 대해 요약, 긍정적 의견, 부정적 의견을 주관적인 감정을 담아 JSON 형식으로 작성해줘.

[설문 평균]
주행 승차감: {analysis_stats['driving_comfort']:.2f}
긴급 상황 대응: {analysis_stats['emergency_response']:.2f}
주차 기능: {analysis_stats['parking_function']:.2f}
전반 만족도: {analysis_stats['overall_satisfaction']:.2f}

출력 형식:
{{
  "driving_comfort": {{
    "summary": "...",
    "positive_opinion": "...",
    "negative_opinion": "..."
  }},
  "emergency_response": {{
    "summary": "...",
    "positive_opinion": "...",
    "negative_opinion": "..."
  }},
  "parking_function": {{
    "summary": "...",
    "positive_opinion": "...",
    "negative_opinion": "..."
  }},
  "overall_satisfaction": {{
    "summary": "...",
    "positive_opinion": "...",
    "negative_opinion": "..."
  }}
}}

주의: 반드시 JSON 형식으로만 응답해줘.
"""
    return prompt
