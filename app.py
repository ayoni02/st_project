import streamlit as st
import google.generativeai as palm
import re
import docx

def auth():
    st.write('Please enter your palm key: ')
    key = st.text_input('Enter your palm key: ')
    return key

def get_doc():
    d = st.file_uploader('Upload your document: ')
    doc = docx.Document(d)

    dtxt = []
    for a in doc.paragraphs:
        if re.search(r"[0-9A-Fa-f]+", a.text):
            dtxt.append(a.text)
        else:
            continue
    return '\n'.join(x for x in dtxt)

def get_prompt(dprompt):
    dtype = st.text_input("Input document type (e.g tecnical) :")
    audience = st.text_input("Input your target audience (e.g developers): ")
    goal = st.text_input("What is your goal for the document (e.g. 'users onboarding for a seamless app journey/UX'): ")
    tone = st.text_input("What tone should the document carry (e.g professional): ")
    prompt =f"""
        I would like to generate a {dtype} document for {audience} to provide {goal}.

        use the following content to generate the document:
        {dprompt}
        
        and lastly, ensure your tone is {tone}
        """
    return prompt



def result(model, prompt):
    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0,
        # The maximum length of the response
        max_output_tokens=999,
    )
    return completion.result

def main():
    key = auth()
    palm.configure(api_key=key)
    models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
    model = models[0].name
    dprompt = get_doc()
    prompt = get_prompt(dprompt)
    writer = result(model, prompt)
    st.write(writer)
    
main()
