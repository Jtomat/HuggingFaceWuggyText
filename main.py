from transformers import pipeline
import wikipedia
import streamlit as st

st.title("Поговрите с личностью из википедии!")

user_input = st.text_area('С кем хотите поговорить?')
button = st.button('Поговорить')

if user_input and button:
  print("run wikipedia search")
  context = wikipedia.search(user_input)
  pipe = pipeline("question-answering", model="AlexKay/xlm-roberta-large-qa-multilingual-finedtuned-ru")
  text = wikipedia.page(context[0]).content
  print("got wiki page")
  answer_input = st.text_area('Ваш вопрос')
  answer_button = st.button('Спросить')
  exit_button = st.button('Закончить')
  if answer_button and answer_input:
    answer = pipe(question=answer_input, context= text)
    st.write(answer)