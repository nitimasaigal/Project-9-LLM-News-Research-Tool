import streamlit as st
import streamlit_authenticator as stauth
from langchain_config import llm_chain, get_summary

# Define user credentials
credentials = {
    "usernames": {
        "nitimasaigal@gmail.com": {"name": "Nitima Saigal", "password": "Hargun@123"},
        "nitimasaigal": {"name": "Nitima Saigal", "password": "hargun@123"}
    },
    "cookie": {"expiry_days": 30, "key": "cookie_key"},
    "preauthorized": {"emails": ["nitimasaigal@gmail.com"]}
}

# Create the authenticator object
authenticator = stauth.Authenticate(
    credentials,
    cookie_name="auth_cookie",
    cookie_key="cookie_key",
    cookie_expiry_days=30
)

# Define fields for login form
login_fields = {
    "username": {"label": "Username", "type": "text"},
    "password": {"label": "Password", "type": "password"}
}

# Login using the updated method
authentication_status, username, name = authenticator.login(
    fields=login_fields
)

if authentication_status:
    st.sidebar.title('Navigation')
    st.sidebar.write('Select an option below:')
    st.sidebar.button('Home')
    st.sidebar.button('Settings')

    st.title('Equity Research News Tool')
    st.write('Enter your query to get the latest news articles summarized.')

    query = st.text_input('Query')

    if st.button('Get News'):
        if query:
            with st.spinner('Fetching and summarizing news articles...'):
                summaries = get_summary(query)
                response = llm_chain.run({'query': query, 'summaries': summaries})
                # Save query
                with open('queries.txt', 'a') as file:
                    file.write(query + '\n')
            st.success('Done!')
            st.write('### Summary:')
            st.write(response)
            st.download_button(
                label="Download Summary",
                data=response,
                file_name="summary.txt",
                mime="text/plain"
            )
        else:
            st.warning('Please enter a query.')

    st.sidebar.title('Historical Data Analysis')
    if st.sidebar.button('Analyze'):
        with open('queries.txt', 'r') as file:
            queries = file.readlines()
            st.write('### Historical Queries:')
            st.write(queries)
            # Additional analysis can be added here
elif authentication_status is False:
    st.error('Username or password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')
