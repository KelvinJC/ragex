# Create streamlit app

from typing import List, Tuple

import streamlit as st
import requests
 
 
# configure web page
st.set_page_config(page_title="RAG.ai", page_icon="✨", layout="wide")

# initialise session state for tracking user input and responses
if 'responses' not in st.session_state:
    st.session_state.responses = []

def scroll_to_bottom_of_page():
    """ Return focus to bottom of page once a question is entered."""
    # Define the scroll operation as a function and pass in something unique for each
    # page load that it needs to re-evaluate where "bottom" is
    js = f"""
    <script>
        function scroll(dummy_var_to_force_repeat_execution){{
            var textAreas = parent.document.querySelectorAll('section.main');
            for (let index = 0; index < textAreas.length; index++) {{
                textAreas[index].scrollTop = textAreas[index].scrollHeight;
            }}
        }}
        scroll({len(st.session_state.responses)})
    </script>
    """

    js = '''
    <script>
        var body = window.parent.document.querySelector(".main");
        console.log(body);
        body.scrollTop = 0;
    </script>
    '''
    st.components.v1.html(js)

def display_chat_history():
    with st.container():
        for response in st.session_state.responses:
            left, right = st.columns(2)
            right.markdown(f"""
                <div style="background-color:#262730; padding:10px; border-radius:20px;">
                    <p style="font-family:Arial, sans-serif; font-color: #2f2f2f; ">{response['user']}</p>
                </div>
                </br>
                """, 
                unsafe_allow_html=True,
            )
            st.empty().markdown(f"""
                <div style="padding:10px; border-radius:5px;">
                    <p style="font-family:Arial, sans-serif; font-color: #2f2f2f; ">{response['bot']}</p>
                </div>
                </br>
                """, 
                unsafe_allow_html=True,
            )

def post_request_to_api(url: str, question: str, model: str, temperature: float):
    """Send the user input to backend API"""
    response = requests.post(
        url,
        json={
            "question": question,
            "model": model,
            "temperature": temperature,
        },
        stream=True,
    )
    return response

def configure_file_payload(file) -> Tuple:
    return ("files", (file.name, file.read(), "application/pdf"))

def upload_files_to_api(url: str, files: List):
    """Upload files to backend API"""
    all_file_content = [configure_file_payload(file) for file in files]
    response = requests.post(url, files=all_file_content) # stream=True,
    return response

def handle_file_upload(file_input, backend_url): # default selection is Stream
    if not file_input:
        # add user input to session state
        # file_names = ", ".join([file.name for file in file_input])
        st.session_state.responses.append(
            {
                "user": "", 
                "bot": """ Hello I am here to help you understand any any document? Upload the files to start"""
            }
        )
        return 
    
    # add user input to session state
    file_names = ", ".join([file.name for file in file_input])
    st.session_state.responses.append({"user": f"Uploaded files: {file_names}", "bot": None})

    # prepare empty container to update the bot's response in real time
    response_container = st.empty()

    response = upload_files_to_api(url=backend_url, files=file_input)
    res_detail = response.json()
    if response.status_code == 200:
        bot_response = res_detail["detail"]
        # display bot's response with adaptable height
        st.markdown(
            f"""
            <div style="padding:10px; border-radius: 5px;">
                <p style="font-family: Arial, sans-serif; font-color: #2f2f2f">{bot_response.strip()}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # update the latest bot response in session state
        st.session_state.responses[-1]['bot'] = bot_response.strip()

    else:
        response_container.markdown(
            f"""
            <div style="padding:10px; border-radius: 5px;">
                <p style="font-family: Arial, sans-serif; color:red">
                    Error: {res_detail["detail"]}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # update the latest bot response in session state
        st.session_state.responses[-1]['bot'] = res_detail["detail"]
    # clear input box for next question
    # st.session_state.current_input = ""

def handle_message(user_input, backend_url, selected_model, temperature): # default selection is Stream
    if user_input:
        # add user input to session state
        st.session_state.responses.append({'user': user_input, 'bot': None})
        # prepare empty container to update the bot's response in real time
        response_container = st.empty()

        res = post_request_to_api(url=backend_url, question=user_input, model=selected_model, temperature=temperature)
        if res.status_code == 200:
            bot_response = ""
            # if selected_response_type == chatbot.output_type[0]:
            #     # stream response from backend
            #     for chunk in res.iter_content(chunk_size=None, decode_unicode=True):
            #         bot_response += chunk
            #         # update response container with the latest bot response
            #         response_container.markdown(
            #             f"""
            #             <div style="padding:10px; border-radius: 5px;">
            #                 <p style="font-family: Arial, sans-serif; font-color: #2f2f2f">{bot_response.strip()}</p>
            #             </div>
            #             """,
            #             unsafe_allow_html=True,
            #         )
            #         # update the latest bot response in session state
            #         st.session_state.responses[-1]['bot'] = bot_response.strip()

            # else:
            # collect the batch response
            for chunk in res.iter_content(chunk_size=None, decode_unicode=True):
                bot_response += chunk
            
            # display bot's response with adaptable height
            st.markdown(
                f"""
                <div style="padding:10px; border-radius: 5px;">
                    <p style="font-family: Arial, sans-serif; font-color: #2f2f2f">{bot_response.strip()}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            # update the latest bot response in session state
            st.session_state.responses[-1]['bot'] = bot_response.strip()

        else:
            res_content = res.json()
            response_container.markdown(
                f"""
                <div style="padding:10px; border-radius: 5px;">
                    <p style="font-family: Arial, sans-serif; color: red">
                        Error: {res_content["detail"]}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.session_state.responses[-1]['bot'] = res_content["detail"]
        # clear input box for next question
        # st.session_state.current_input = ""

def get_configs():
    with st.sidebar:
        with st.form("🗀 File Input", clear_on_submit=True):
            uploaded_files = st.file_uploader(
                "Upload local files:",
                type=["txt", "pdf", "docx", "csv", "jpg", "png", "jpeg", "py"],
                accept_multiple_files=True,
            )
            submitted = st.form_submit_button("Submit")
        if uploaded_files and submitted:
            st.session_state["uploaded_files"] = uploaded_files

        # expander = st.expander("Select your response type", expanded=True)
        # with expander:
        # select model and training parameters
        expander = st.expander("⚒ RAG Pipeline Configuration", expanded=True)
        with expander:
            st.subheader("Adjust RAG Parameters")
            selected_response_type = st.radio("Output types", ["Stream", "Batch"], index=None)
            temperature = st.slider("Temperature", min_value=0.01, max_value=5.0, value=0.0, step=0.01, format="%.1f")
        selected_model = st.selectbox("Select your preferred model: ", ["llama-3.1-70b-versatile","llama-3.1-8b-instant","mixtral-8x7b-32768"])
        # set_tokens = st.selectbox("Please select length of output", chatbot.token_class.keys())
        return selected_model, selected_response_type, temperature, submitted #, set_tokens


# main layout
def main():
    scroll_to_bottom_of_page()
    display_chat_history()

    # selected_model, selected_response_type, temperature, set_tokens = get_configs()
    selected_model, selected_response_type, temperature, submitted = get_configs()
    # selected_response_type = selected_response_type # if selected_response_type else chatbot.output_type[0] # default selection is Stream 
    
    files = st.session_state.get("uploaded_files")
    if submitted:
        handle_file_upload(file_input=files, backend_url="http://127.0.0.1:8888/upload")
        scroll_to_bottom_of_page()

    # collect user input below the chat history
    prompt = st.chat_input("Ask a question")
    if prompt:
        user_input = prompt

        # define the URL of the backend API
        # if selected_response_type == chatbot.output_type[0]:
        #     backend_url = "http://127.0.0.1:5000/chat_stream"
        # else:
        backend_url = "http://127.0.0.1:8888/generate"
        
        if user_input:
            left, right = st.columns(2)
            right.markdown(f"""
            <div style="background-color:#262730; padding:10px; bottom-margin: 1px; border-radius:20px;">
                <p style="font-family:Arial, sans-serif; font-color: #2f2f2f; ">{user_input}</p>
            </div>
            </br>
            """, 
            unsafe_allow_html=True)
            handle_message(
                user_input=user_input,
                backend_url=backend_url,
                selected_model=selected_model,
                temperature=temperature,
            )

if __name__ =="__main__":
    main()