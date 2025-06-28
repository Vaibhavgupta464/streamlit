import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
import requests
import json
import os

# Set page configuration
st.set_page_config(page_title="Data Engineering Pipeline Demo with AI", layout="wide")

# Title and description
st.title("Data Engineering Pipeline Demo with AI")
st.markdown("""
This app demonstrates a data engineering pipeline with AI integration. Upload a CSV file, clean and transform the data, 
visualize the results, and use the AI chat to ask data engineering questions or analyze your dataset.
""")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Sidebar for AI Chat
with st.sidebar:
    st.subheader("AI Assistant (Powered by open ai 3)")
    st.markdown("Ask questions about data engineering or your dataset!")
    
    # Example prompts
    st.markdown("**Example Questions:**")
    st.markdown("- What is ETL in data engineering?")
    st.markdown("- How should I handle missing values in my dataset?")
    st.markdown("- Analyze my dataset and suggest transformations.")
    
    # API Key input
    api_key = st.text_input("Enter xAI API Key", type="password")
    if not api_key:
        st.warning("Please enter your xAI API key to use the AI assistant.")
    
    # Chat input
    user_query = st.text_input("Your question:")
    if st.button("Ask AI") and user_query and api_key:
        try:
            # Prepare dataset context if a file is uploaded
            dataset_context = ""
            if 'df' in locals():
                dataset_context = f"Dataset Info: {df.shape[0]} rows, {df.shape[1]} columns. Columns: {', '.join(df.columns)}. Sample data: {df.head(3).to_dict()}"
            
            # Make API call to xAI's open ai 3
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a data engineering expert. Provide concise, accurate answers related to data engineering concepts or the user's dataset."},
                    {"role": "user", "content": f"{user_query}\n{dataset_context}"}
                ]
            }
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            ai_response = response.json()['choices'][0]['message']['content']
            
            # Store in chat history
            st.session_state.chat_history.append({"user": user_query, "ai": ai_response})
            
        except Exception as e:
            st.error(f"Error with AI API: {str(e)}")
    
    # Display chat history
    if st.session_state.chat_history:
        st.subheader("Chat History")
        for chat in st.session_state.chat_history:
            st.markdown(f"**You**: {chat['user']}")
            st.markdown(f"**AI**: {chat['ai']}")
            st.markdown("---")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file
    try:
        df = pd.read_csv(uploaded_file)
        st.success("File successfully uploaded!")
        
        # Display raw data
        st.subheader("Raw Data Preview")
        st.dataframe(df.head())

        # Data Info
        st.subheader("Data Information")
        buffer = StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())

        # Data Cleaning Section
        st.subheader("Data Cleaning")
        st.markdown("Handle missing values and select columns for analysis.")

        # Handle missing values
        missing_option = st.selectbox(
            "How to handle missing values?",
            ["Drop rows with missing values", "Fill with mean", "Fill with median", "Fill with mode"]
        )

        if missing_option == "Drop rows with missing values":
            cleaned_df = df.dropna()
        elif missing_option == "Fill with mean":
            cleaned_df = df.fillna(df.select_dtypes(include=['float64', 'int64']).mean())
        elif missing_option == "Fill with median":
            cleaned_df = df.fillna(df.select_dtypes(include=['float64', 'int64']).median())
        else:
            cleaned_df = df.fillna(df.select_dtypes(include=['object']).mode().iloc[0])

        st.write(f"Rows after cleaning: {cleaned_df.shape[0]} (Original: {df.shape[0]})")
        
        # Select columns for transformation
        numeric_columns = cleaned_df.select_dtypes(include=['float64', 'int64']).columns
        selected_column = st.selectbox("Select a numeric column for transformation", numeric_columns)

        # Transformation Section
        st.subheader("Data Transformation")
        transformation = st.selectbox(
            "Apply transformation",
            ["None", "Log Transform", "Standard Scaling", "Min-Max Scaling"]
        )

        transformed_df = cleaned_df.copy()
        if transformation == "Log Transform":
            transformed_df[selected_column] = cleaned_df[selected_column].apply(lambda x: pd.np.log(x + 1) if x > 0 else 0)
        elif transformation == "Standard Scaling":
            transformed_df[selected_column] = (cleaned_df[selected_column] - cleaned_df[selected_column].mean()) / cleaned_df[selected_column].std()
        elif transformation == "Min-Max Scaling":
            transformed_df[selected_column] = (cleaned_df[selected_column] - cleaned_df[selected_column].min()) / (cleaned_df[selected_column].max() - cleaned_df[selected_column].min())

        st.dataframe(transformed_df[[selected_column]].head())

        # Visualization Section
        st.subheader("Data Visualization")
        viz_type = st.selectbox("Select visualization type", ["Histogram", "Box Plot", "Scatter Plot"])

        fig, ax = plt.subplots()
        if viz_type == "Histogram":
            sns.histplot(transformed_df[selected_column], ax=ax)
            ax.set_title(f"Histogram of {selected_column}")
        elif viz_type == "Box Plot":
            sns.boxplot(y=transformed_df[selected_column], ax=ax)
            ax.set_title(f"Box Plot of {selected_column}")
        elif viz_type == "Scatter Plot":
            if len(numeric_columns) > 1:
                second_column = st.selectbox("Select second column for scatter plot", [col for col in numeric_columns if col != selected_column])
                sns.scatterplot(x=transformed_df[selected_column], y=transformed_df[second_column], ax=ax)
                ax.set_title(f"Scatter Plot: {selected_column} vs {second_column}")
            else:
                st.warning("Need at least two numeric columns for scatter plot.")
        
        st.pyplot(fig)

        # Download cleaned and transformed data
        st.subheader("Download Processed Data")
        csv = transformed_df.to_csv(index=False)
        st.download_button(
            label="Download processed data as CSV",
            data=csv,
            file_name="processed_data.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
else:
    st.info("Please upload a CSV file to begin.")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit | Powered by xAI's open ai 3 | Learn Data Engineering Concepts")
