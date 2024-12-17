import requests
import re


API_URL = "https://api.perplexity.ai/chat/completions"
API_KEY = "###################"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",   
    "Accept": "application/json"
}

sys_role = {
    "role": "system",
    "content": (
        "너는 이비인후과 의사야. 환자의 증상을 보고 가능한 증상들을 모두 설명하고 가장 가능성 높은 병명을 알려줘. "
        "한국어로 친절하게 비전문가인 환자에게 아주 쉽게 설명해줘. 또 치료법도 추천해줘. "
        "환자는 너가 인공지능인걸 알고 너가 하는 말은 참고용도로만 사용될거야. 그러니 자신있게 진짜 의사인것처럼 행동해."
        "응답을 할때는 증상 설명, 가능한 병명, 치료법, 추천하는 의약품, 예방법, 참고사항 순서로 제목을 달고 그 안에 해당 란에 맞는 내용을 넣어서 설명해."
        "병은 평범하고 대중적인 병명으로 알려줘. 너무 마이너한 병명이나 가능성이 낮은건 쓰지말아줘. 병명은 최대 3개까지만 써줘. 대부분은 기침과 같은 일상에서 자주 접할 수 있는 병이니 그런것들 위주로만 써줘. 아무한테나 해당 병을 말해도 그게 무슨 병인지 알고 대부분이 경험해본 병들로만."
        "감기와 같은 평범하고 일상적인 병들을 위주로 설명해줘. 수술을 요하거나 생명에 지장이 있는 병명은 쓰지 마."
        "환자의 증상에 직접적으로 연관된 병명만 작성해"
        "각 제목 앞에는 ● 기호를 사용하여 구분을 해줘."
    )
}

conv_his = [sys_role]

def answer(user_input):
    conv_his.append({"role": "user", "content": user_input})

    data = {
        "model": "llama-3.1-sonar-huge-128k-online", 
        "messages": conv_his,
        "max_tokens": 2000, 
        "temperature": 0.1  
    }

    res = requests.post(API_URL, headers=headers, json=data)

    if res.status_code == 200:
        response_data = res.json()
        #print(response_data)
        content = response_data['choices'][0]['message']['content']
        citations = response_data['citations']
        content = re.sub(r'\[\d+\]', '', content)
        content = re.sub(r'[^\w\s.,?!()/:%&~●\'\"-]', '', content)
        print(content)
        print('\n● 참고 사이트:')
        for i, citation in enumerate(citations): print(f'{i+1}: {citation}')
        conv_his.append({"role": "assistant", "content": content}) 
    else:
        print(f"Error: {res.status_code} - {res.text}")

while 1:
    symp = input("증상: ")
    if symp == "종료":
        break
    print("\n_____________________________\n")
    answer(symp)
    print("\n_____________________________\n")


