import os
from dotenv import load_dotenv

import json

import google.generativeai as genai


load_dotenv()

model = genai.GenerativeModel(os.getenv('MODEL_TYPE'))

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


def print_available_model():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)

def prepare_prompt(resume, tech_stack, difficulty, question_count):
    with open("GeminiAPI/prompt_question.txt", "r") as file:
        prompt = file.read()

    prompt = prompt.replace("{resume}", resume)
    prompt = prompt.replace("{tech_stack}", tech_stack)
    prompt = prompt.replace("{difficulty}", str(difficulty))
    prompt = prompt.replace("{question_count}", str(question_count))

    return prompt

def get_questions(prompt):
    response = model.generate_content(prompt)
    questions = response.text.split('QQQ')
    questions = [question for question in questions if '\n' not in question]
    return questions



if __name__=='__main__':
    prompt = prepare_prompt(resume='Aaryan Regmi \n Python\n machine learning \n Face Recognition project \n aaryanreegmi39@gmail.com', tech_stack='python, machine learning', difficulty=2, question_count=5)
    print(prompt)
    questions = get_questions(prompt)
    print(questions)



