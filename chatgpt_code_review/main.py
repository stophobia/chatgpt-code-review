import logging
import os

import openai
import streamlit as st
from about import about_section
from functions import display_code, escape_markdown, get_recommendations

# Set up the OpenAI API
# Load the API key from .env
env_file_path = ".env"

# Load all environment variables from the .env file
if os.path.exists(env_file_path):
    with open(env_file_path) as f:
        for line in f:
            if line.strip():
                key, value = line.strip().split("=")
                os.environ[key] = value

# Configure logging
log_file = "app.log"
logging.basicConfig(filename=log_file, level=logging.INFO)

st.set_page_config(
    page_title="ChatGPT Code Review",
    page_icon=":robot_face:",
    layout="wide",
    initial_sidebar_state="expanded",
)


button = False

# Sidebar with links to OpenAPI and the GitHub repository
with st.sidebar:
    st.markdown(
        """
        <!--don't underline links -->
        <style>
        a {
            text-decoration: none;
        }
        </style>
        ## Links

        :robot_face:  [OpenAI](https://openai.com/)

        :key:  [API Keys](https://platform.openai.com/account/api-keys)

        :toolbox:  [GitHub](https://github.com/domvwt/chatgpt-code-review)
        """,
        unsafe_allow_html=True,
    )

c1, c2, c3 = st.columns([1, 8, 1])

with c2:
    st.title("ChatGPT Code Review :rocket:")

    # About section expanded by default
    with st.expander("About ChatGPT Code Review"):
        st.markdown(about_section)

    with st.form("repo_url_form"):
        # Get the GitHub repository URL
        default_repo_url = "https://github.com/domvwt/chatgpt-code-review"
        repo_url = st.text_input("GitHub Repository URL:", default_repo_url)

        # Show the API key
        api_key = os.getenv("OPENAI_API_KEY", "your-api-key")
        openai.api_key = st.text_input("OpenAI API Key:", api_key)

        # Set the maximum as integer input
        max_tokens = st.number_input(
            "Maximum tokens per OpenAI API response", min_value=1, max_value=4096, value=200
        )

        button = st.form_submit_button("Analyze Repository")

    if button:
        with st.spinner("Analyzing repository..."):
            if repo_url:
                recommendations = get_recommendations(repo_url, max_tokens)

                # Display the recommendations
                first = True
                for rec in filter(None, recommendations):
                    if not first:
                        st.write("---")
                    else:
                        st.header("Recommendations")
                        first = False
                    subheader = escape_markdown(rec["code_file"]).replace("/tmp/", "")
                    st.subheader(subheader)
                    recommendation = rec["recommendation"] or "No recommendations"
                    st.markdown(recommendation)
                    # Expander to show the code
                    with st.expander("View Code"):
                        display_code(rec["code_snippet"], "python")
            else:
                st.error("Please enter a valid GitHub repository URL.")