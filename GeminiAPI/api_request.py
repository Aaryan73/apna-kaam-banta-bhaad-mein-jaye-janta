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

def calculate_percentage(result_list, marking):
    total_points = 0
    max_points = 0

    for result in result_list:
        if result in marking:
            total_points += marking[result]
            max_points += marking['Completely correct']

    percentage = (total_points / max_points) * 100
    rounded_percentage = (percentage // 10) * 10

    return rounded_percentage

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

def prepare_prompt_for_answercheck(question_answer_pair):
    with open("GeminiAPI/prompt_check_answer.txt", "r") as file:
        prompt = file.read()
    qa_string = ""
    for key, value in question_answer_pair.items():
        qa_string += f"\nquestion: {key}\n"
        qa_string += f"answer: {value}\n"
    prompt = prompt.replace("{question_answer_pair}", qa_string.strip())
    
    return prompt

def get_evaluation(prompt):
    response = model.generate_content(prompt)
    evaluation = [evaluation.strip(' ') for evaluation in response.text.split('QQQ') if evaluation.strip(' ') in ['Incorrect', 'Partially correct', 'Completely correct']]
    marking = {
        'Completely correct':10,
        'Incorrect':0,
        'Partially correct':5
    }
    score = calculate_percentage(evaluation, marking)
    return score


if __name__=='__main__':
    prompt = prepare_prompt_for_answercheck(question_answer_pair={'what are the 3 primary colors?': 'Red Green and Blue', 'What is python?':'Python is a low level programming language.'})
    print(prompt)
    score = get_evaluation(prompt)
    print(score)



