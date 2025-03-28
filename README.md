#### python을 데이터 중심으로 관리 및 학습하여 배우는 것이 목표입니다. 

python, numpy, pandas, data analysitics 


## python 확장명 

> - .ipynb 
> - .py 


## python 실행 

```
python  main.py 
```

## Streamlit 실행 

```
streamlit run app.py 
```

```
cd .\pandas\
```


## 실행 범위만 실행 
```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```


## 가상환경 설치 
```
pyton3 -m venv venv 
```

```
.\venv\Scripts\activate
```

```
pip install -r requirements.txt 
```
cd self_driving_feedback
streamlit run app.py
```
streamlit run .\streamlit_1_chart.py
```

 pip install ipykernel -U --force-reinstall --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

## pip install 

```
pip freeze > requirements.txt 
```
```
pip install -r requirements.txt 
```
########################################################################3

### 자동차 자율 주행 실행하는 방법 

```
 pip install -r requirements.txt  
```

```
 cd self_driving_feedback
 ls  ### (app.py가 있는지 확인) 
 streamlit run app.py
```

```
  https://platform.openai.com/docs/overview
```

streamlit run pdf_run.py

자동차 자율 주행 만족도 평가 설문지가 동작됩니다.  


{
"driving_comfort":3
"emergency_response":3.06
"parking_function":3.03
"overall_satisfaction":3.07
}
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
