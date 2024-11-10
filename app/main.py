import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://www.google.com/about/careers/applications/jobs/results/124204114060944070-associate-product-manager-university-graduate-2025-start?category=DATA_CENTER_OPERATIONS&category=DEVELOPER_RELATIONS&category=HARDWARE_ENGINEERING&category=INFORMATION_TECHNOLOGY&category=MANUFACTURING_SUPPLY_CHAIN&category=NETWORK_ENGINEERING&category=PRODUCT_MANAGEMENT&category=PROGRAM_MANAGEMENT&category=SOFTWARE_ENGINEERING&category=TECHNICAL_INFRASTRUCTURE_ENGINEERING&category=TECHNICAL_SOLUTIONS&category=TECHNICAL_WRITING&category=USER_EXPERIENCE&employment_type=FULL_TIME&employment_type=PART_TIME&employment_type=TEMPORARY&jex=ENTRY_LEVEL")
    submit_button = st.button("Submit")

    if submit_button:
        #try:
        loader = WebBaseLoader([url_input])
        data = clean_text(loader.load().pop().page_content)
        portfolio.load_portfolio()
        jobs = llm.extract_jobs(data)
        #st.write(jobs)
        for job in jobs:
            skills = job.get('skills', [])
            links = portfolio.query_links(skills)
            email = llm.write_mail(job, links)
            st.code(email, language='markdown')
        #except Exception as e:
           # st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)


