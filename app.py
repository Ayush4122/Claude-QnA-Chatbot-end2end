import streamlit as st
import requests
from bs4 import BeautifulSoup
from anthropic import Anthropic

# Initialize Anthropic client
anthropic = Anthropic(api_key="YOUR-CLAUDE-KEY")

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = ' '.join([p.get_text() for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])])
        return text
    except requests.RequestException as e:
        st.error(f"Error scraping website: {e}")
        return None

def get_claude_response(query, context):
    try:
        response = anthropic.completions.create(
            model="claude-3-sonnet-20240229",
            max_tokens_to_sample=1000,
            temperature=0.7,
            prompt=f"""Human: You are an AI assistant for a specific website. Use the following context to answer the user's question. If you can't answer based on the context, say so politely.

Context:
{context}

User question: {query}

Assistant: Based on the provided context, I can offer the following response:
"""
        )
        return response.completion
    except Exception as e:
        st.error(f"Error getting Claude response: {e}")
        return "I'm sorry, I encountered an error while processing your request."

def main():
    st.title("Website Q&A Assistant")

    # Input for website URL
    website_url = st.text_input("Enter website URL:")
    
    # Button to process website content
    if st.button("Process Website"):
        if website_url:
            with st.spinner("Processing website content..."):
                content = scrape_website(website_url)
                if content:
                    st.session_state['website_content'] = content
                    st.success("Website content processed successfully!")
                else:
                    st.error("Failed to process website content. Please check the URL and try again.")
        else:
            st.warning("Please enter a website URL.")

    # Input for user question
    user_question = st.text_input("Ask a question about the website:")

    # Button to get response
    if st.button("Get Answer"):
        if user_question and 'website_content' in st.session_state:
            with st.spinner("Getting answer..."):
                response = get_claude_response(user_question, st.session_state['website_content'])
            st.write("Answer:", response)
        elif 'website_content' not in st.session_state:
            st.warning("Please process a website first.")
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
