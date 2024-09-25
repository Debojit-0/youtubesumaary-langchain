import validators # validates the url
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader #UnstructuredURLLoader ---> directly the url we can load thr content


#streamlit app
st.set_page_config(page_title="Langchain:Summarize Text from Youtube")
st.title("Langchain: Summarize Text from Youtube or Website")
st.subheader("Summarize URL")



# get the groq api key and url  to be summarised
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key",value="",type="password")

genric_url=st.text_input("URL",label_visibility="collapsed")


# initialize ur model
llm = ChatGroq(api_key=groq_api_key,model_name="Gemma2-9b-It",streaming=True)

#Creating the promt template
promt_template = """Provide summary of the following content in 300 words:
Content:{text}

"""
prompt=PromptTemplate(template=promt_template,input_variables=["text"])

if st.button("Summarize the content from Youtube or Website"):
    if not groq_api_key.strip() or not genric_url.strip():
        st.error("Please provide the information")
    elif not validators.url(genric_url):
        st.erroR("Please enter valid Url it can either be a youtube url or a website url")
    else:
        try:
            with st.spinner("waiting..."):
                ## loading the website or youtube video data
                if "youtube.com" in  genric_url:
                    loader = YoutubeLoader.from_youtube_url(genric_url,add_video_info=True)
                else:
                    loader=UnstructuredURLLoader(urls=[genric_url],ssl_verify=False,headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                


                docs= loader.load()

                # creating the chain for sumamrisation

                chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)

                # run the summary
                output_summary=chain.run(docs)

                st.success(output_summary)
        except Exception as e:
            st.exception(f"Exception:{e}")



