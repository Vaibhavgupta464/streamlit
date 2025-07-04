# DAG Dependency Explorer

A Streamlit app to explore DAG (Directed Acyclic Graph) dependencies.

## Features

- Upload a JSON file containing DAG dependencies.
- Input a DAG name and find its upstream and downstream DAGs.
- View relevant DAGs (upstream + current + downstream) clearly.
- Uses a sample JSON by default if no file is uploaded.

## JSON Format

The uploaded JSON should be a dictionary where:

- Keys = DAG names
- Values = list of downstream DAG names

Example:

```json
{
  "dag_name_1": ["child_dag_1", "child_dag_2"],
  "dag_name_2": ["child_dag_3"]
}
```

## How to Run
Make sure you have Python installed (version 3.7+ recommended).

## Install Streamlit if you haven't yet:
- pip install streamlit
- Save the app code as app.py.

## Run the app:
- streamlit run app.py

Upload your DAG dependency JSON or use the sample.

Enter a DAG name to explore dependencies.
