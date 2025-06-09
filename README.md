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
