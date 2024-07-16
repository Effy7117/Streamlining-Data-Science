from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import subprocess

# Function to train the model using the Python script
def train_model():
    subprocess.call(['python3', '/home/effy/deaths-leading-causes.py'])

# Default arguments for the DAG
default_args = {
    'owner': 'Effy',
    'start_date': datetime(2024, 7, 14),
    'schedule_interval': '@daily',
}

# Initialize the DAG
dag = DAG(
    'deaths-leading-causes-dag',
    default_args=default_args,
    schedule_interval='@daily',
)

extract_data = PythonOperator(
    task_id='extract_data',
    python_callable=lambda: subprocess.call(['bash', '/home/effy/deaths-leading-causes-extract.sh']),
    dag=dag,
)

remove_duplicates_task = PythonOperator(
    task_id='remove_duplicates',
    python_callable=lambda: subprocess.call(['bash', '/home/effy/deaths-leading-causes-transform-remove-duplicates.sh']),
    dag=dag,
)

handle_missing_values_task = PythonOperator(
    task_id='handle_missing_values',
    python_callable=lambda: subprocess.call(['bash', '/home/effy/deaths-leading-causes-transform-handle-missing-values.sh']),
    dag=dag,
)

clean_numeric_columns_task = PythonOperator(
    task_id='clean_numeric_columns',
    python_callable=lambda: subprocess.call(['bash', '/home/effy/deaths-leading-causes-transform-clean-numeric-columns.sh']),
    dag=dag,
)

encode_categorical_task = PythonOperator(
    task_id='encode_categorical',
    python_callable=lambda: subprocess.call(['bash', '/home/effy/deaths-leading-causes-transform-encode-categorical.sh']),
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=lambda: subprocess.call(['bash', '/home/effy/deaths-leading-causes-load.sh']),
    dag=dag,
)

train_model_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag,
)

# Task dependencies
extract_data >> [remove_duplicates_task, handle_missing_values_task]
remove_duplicates_task >> clean_numeric_columns_task
handle_missing_values_task >> clean_numeric_columns_task
clean_numeric_columns_task >> encode_categorical_task
encode_categorical_task >> load_task >> train_model_task

