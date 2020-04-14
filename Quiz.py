from Question import Question

question_prompts = [
    "What is the capital of Turkey?\n(a) Istanbul\n(b) Ankara\n(c) Antalya\n\n",
    "What is the largest snake on Earth?\n(a) Boa Constrictor\n(b) Burmese Python\n(c) Anaconda\n\n",	
    "Which country is the origin of the cocktail Mojito?\n(a) Cuba\n(b) Argentina\n(c) Mexico\n\n",

]

questions = [
    Question(question_prompts[0], "b"),
    Question(question_prompts[1], "c"),
    Question(question_prompts[2], "a"),
]

def run_test(questions):
    score = 0
    for question in questions:
        answer = input(question.prompt)
        if answer == question.answer:
            score += 1
    print("You got " + str(score) + "/" + str(len(questions)) + " Correct")

run_test(questions)
