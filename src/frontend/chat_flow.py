import streamlit as st

 
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
