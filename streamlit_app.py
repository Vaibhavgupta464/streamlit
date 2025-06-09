import streamlit as st
import json

st.title("DAG Dependency Explorer")

st.markdown("""
Upload a JSON file containing DAG dependencies in this format:

```json
{
  "dag_name_1": ["child_dag_1", "child_dag_2"],
  "dag_name_2": ["child_dag_3"]
}
Then enter a DAG name to see its upstream and downstream DAGs.
""")

#Upload JSON file
uploaded_file = st.file_uploader("Upload DAG dependency JSON file", type=["json"])

#Sample JSON if user wants to try without uploading
sample_json = {
'i0001_ivo_hdr_weekly': ['i0001_ivo_hdr_daily', 'i0001_ivo_hdr_daily'],
'i0002_ivo_dtl_weekly': ['i0002_ivo_dtl_daily'],
'i1146_pnr_gfc_daily': ['i1147_gfc_tns'],
'i1146_pnr_gfc_weekly': ['i1147_gfc_tns'],
'i1148_lws_gfc_weekly': ['i1147_gfc_tns', 'i1148_lws_gfc_daily'],
'i1147_gfc_tns_weekly': ['i1148_lws_gfc_weekly'],
'i1607_i1769_recycle_daily_dag': ['i1607_i1769_inc_daily_dag'],
'i1608_pra_not_rvu_ivo_tnd_mf_daily': ['i0675_acu_bus_crd_ivo_daily_dag'],
'i1608_pra_not_rvu_ivo_tnd_talend': ['i1608_pra_not_rvu_ivo_tnd_mf_daily', 'i1608_pra_not_rvu_ivo_tnd_weekly']
}

if uploaded_file:
    try:
        dag_dependency_config = json.load(uploaded_file)
        st.success("JSON loaded successfully!")
    except Exception as e:
        st.error(f"Failed to load JSON: {e}")
        dag_dependency_config = None
else:
    st.info("Using sample DAG dependency config. Upload your own JSON file to replace.")
    dag_dependency_config = sample_json

def get_upstream_dags(dag_name, dependency_map):
    return [parent for parent, children in dependency_map.items() if dag_name in children]

def get_downstream_dags(dag_name, dependency_map):
    return dependency_map.get(dag_name, [])

def generate_check_tasks(dag_name, dag_dependency_config):
    if not dag_name:
        st.error("dag_name not provided")
        return [], [], set()


    upstream_dags = get_upstream_dags(dag_name, dag_dependency_config)
    downstream_dags = get_downstream_dags(dag_name, dag_dependency_config)

    relevant_dags = set(upstream_dags + [dag_name] + downstream_dags)
    return upstream_dags, downstream_dags, relevant_dags

#Ask user for DAG name
dag_name_input = st.text_input("Enter DAG name to query:", "")

if dag_name_input:
    upstream, downstream, relevant = generate_check_tasks(dag_name_input, dag_dependency_config)
    st.markdown("### Results:")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Upstream DAGs")
        if upstream:
            for dag in upstream:
                st.success(dag)
        else:
            st.info("No upstream DAGs found.")

    with col2:
        st.subheader("Entered DAG")
        st.warning(dag_name_input)

    with col3:
        st.subheader("Downstream DAGs")
        if downstream:
            for dag in downstream:
                st.success(dag)
        else:
            st.info("No downstream DAGs found.")

    st.markdown("---")
    st.subheader("All Relevant DAGs (Upstream + Current + Downstream)")
    if relevant:
        st.write(", ".join(sorted(relevant)))
    else:
        st.info("No relevant DAGs found.")
else:
    st.info("Please enter a DAG name above to see dependencies.")
