from transformers import pipeline
import wikipedia
import streamlit as st

st.title("Поговорите с личностью из википедии!")

user_input = st.text_area('С кем хотите поговорить?')
button = st.button('Поговорить')

if user_input and button:
    print("search wikipedia page")
    st.session_state['pipeline'] = pipeline("question-answering",
                                            model="AlexKay/xlm-roberta-large-qa-multilingual-finedtuned-ru")
    context = wikipedia.search(user_input)
    st.session_state["text"] = wikipedia.page(context[0]).content
    print("got wikipedia article")

answer_input = st.text_area('Ваш вопрос')
answer_button = st.button('Спросить')

if answer_input and answer_button:
    print("start answer search")
    pipe = st.session_state['pipeline']
    answer = pipe(question=answer_input, context=st.session_state["text"])
    st.write(answer['answer'])
    print("found answer")
print("end of program")
