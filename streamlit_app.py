import streamlit as st
import anthropic
from langchain_core.messages import AIMessage, HumanMessage
anthropic_api_key = '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'
file_name = "book.pdf"
chat_title = '18 Startup'

client = anthropic.Anthropic(   
    api_key=anthropic_api_key
)

files = client.beta.files.list()
for file in files:
    if file.filename == "book.pdf":
        file_id = file.id
        print(file_id)
        break

def get_response(query):
    response = client.beta.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "use conent from the documet and use first person language for anwering th query. " +  query 
                    },
                    {
                        "type": "document",
                        "source": {
                            "type": "file",
                            "file_id": file_id
                        }
                    }
                ]
            }
        ],
        betas=["files-api-2025-04-14"]
    )
    return response.content[0].text




st.set_page_config(page_title=chat_title, page_icon="🤖")
st.title(chat_title)
if "context_log" not in st.session_state:
    st.session_state.context_log = ["Retrieved context will be displayed here"]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [AIMessage(content=f"Hi, Let's look into {chat_title}")]
result = st.toggle("Toggle Context")
if result:
    st.write(st.session_state.context_log)


for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)


user_query = st.chat_input("Type your question here...")
if user_query is not None and user_query != "":    
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    
    with st.chat_message("Human"):
        st.markdown(user_query)
    
    with st.chat_message("AI"):
        response = st.write(get_response(user_query))    
 