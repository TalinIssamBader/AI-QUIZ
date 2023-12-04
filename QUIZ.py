# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 11:27:17 2023

@author: Talin
"""

#-----------------------1- import Libraries-------------------------------------
#OpenAI library: allows to use OpenAI's Chat Completion API.
#Random library: used to shuffle the answer options in the quiz.
#Streamlit library:Used to create a user interface for the quiz.
import openai
import random
import streamlit as st


#--------------------------------------------------------------------------------
#---------------2- Initialize OpenAI Chat Completion API with  API key-----------
#--------------------------------------------------------------------------------
openai.api_key = "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"



#-----3- "davinci" for generating the quiz questions and answer options because it is a creative engine 
#that is good at generating interesting and original text. This is important for a quiz, as the
# questions and answer options should be engaging and challenging for the user. "curie" is a factual engine
# that is better at generating accurate information,but it may not be as good at generating creative content.
# Specify the engine to use for generating text (e.g., "davinci" for creative, "curie" for informative)
engine = "davinci"  



#--------------------------------------------------------------------------------
    #Creat function "generate_quiz" that takes a topic and a number of questions 
    #as input and returns a list of dictionaries. Each dictionary contains a question,
                 #four answer options, and the correct answer.
                 
    #	The function uses the OpenAI Chat Completion API to generate the question and 
    #answer options. It first generates a multiple-choice question on the specified topic.
    #Then, it generates four answer options for the question, one of which is the correct answer.
         #Finally, it shuffles the answer options and adds the question data to a list.        
#--------------------------------------------------------------------------------
def generate_quiz(topic, num_questions):
    questions = []

    for _ in range(num_questions):
        # Generate a multiple-choice question on the specified topic using the LangChain API
        question_response = openai.Completion.create(
            prompt="Generate a multiple-choice question on the topic of " + topic,
            engine=engine,)["choices"][0]["text"]
        question_response = question_response.strip()  # Remove leading and trailing whitespace

        # Generate four answer options for the question using the LangChain API
        answer_options = []
        for i in range(4):
            answer_option_response = openai.Completion.create(
                prompt="Generate an answer option for the question: " + question_response,
                engine=engine,  # Specify the engine here
            )["choices"][0]["text"]
            answer_option_response = answer_option_response.strip()  # Remove leading and trailing whitespace
            answer_options.append(answer_option_response)

        # Append the correct answer to the answer options
        correct_answer = random.choice(answer_options)
        answer_options.append(correct_answer)

        # Shuffle the answer options to randomize the order
        random.shuffle(answer_options)

        # Create a dictionary to store the question, answer options, and correct answer
        question_data = {
            "question": question_response,
            "answer_options": answer_options,
            "correct_answer": correct_answer,
        }

        # Add the question data to the list of questions
        questions.append(question_data)

    return questions



#--------------------------------------------------------------------------------
# ------------Create the Streamlit application with a title---------------------
#--------------------------------------------------------------------------------
st.title("MCQ Quiz")



#--------------------------------------------------------------------------------
# ---------Allow users to input their desired quiz topic and number of questions-----
#--------------------------------------------------------------------------------

topic = st.text_input("Enter your desired quiz topic:")
num_questions = int(st.number_input("Enter the number of questions:"))



#--------------------------------------------------------------------------------
#-------- Use if statment to Generate the quiz based on the user's input----------
#--------------------------------------------------------------------------------

if st.button("Generate Quiz"):
    if topic and num_questions > 0:
        questions = generate_quiz(topic, num_questions)

        # Display the generated quiz questions and answer options one by one
        for question in questions:
            st.subheader(question["question"])

            answer_options = question["answer_options"]
            for option in answer_options:
                selected_answer = st.radio(answer_options.index(option), option)

                if selected_answer:
                    break

            # Display a "Next Question" button to proceed to the next question
            if st.button("Next Question"):
                break



#--------------------------------------------------------------------------------
#------------ Calculate the quiz score by comparing selected answers to correct answers----------
#--------------------------------------------------------------------------------

        correct_answers = 0
        for question in questions:
            if question["correct_answer"] == selected_answer:
                correct_answers += 1

        score = (correct_answers / num_questions) * 100
        st.title("Quiz Results")
        st.write("Your score: " + str(score) + "%")

        # Display the correct answers for each question
        for question in questions:
            st.write(question["question"])
            st.write("Correct answer: " + question["correct_answer"])
            st.write("Your answer: " + selected_answer)


            
        

