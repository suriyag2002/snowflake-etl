import os
import pandas as pd
import boto3
import streamlit as st
from io import StringIO
from dotenv import load_dotenv
import snowflake.connector
from groq import Groq
import re
from botocore.exceptions import NoCredentialsError

load_dotenv()

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

st.title("Ask questions about your Snowflake data in natural language! 💬")

db_choice = st.selectbox("🔹 Choose a database:", ["DEMO_DB", "SAMPLE_DB"])

def get_snowflake_connection(database):
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=database,
        schema="PUBLIC",
        role=os.getenv("SNOWFLAKE_ROLE")
    )

def get_schema_info(database):
    conn = get_snowflake_connection(database)
    cur = conn.cursor()
    
    cur.execute(f"""
        SELECT table_name 
        FROM {database}.INFORMATION_SCHEMA.TABLES
        WHERE table_schema = 'PUBLIC';
    """)
    
    tables = cur.fetchall()

    schema_info = f"\n📚 Database: {database} Schema Information:\n"
    for table in tables:
        table_name = table[0]
        
        cur.execute(f"""
            SELECT column_name, data_type
            FROM {database}.INFORMATION_SCHEMA.COLUMNS
            WHERE table_schema = 'PUBLIC' AND table_name = '{table_name}';
        """)
        
        columns = cur.fetchall()
        schema_info += f"\nTable: {table_name}\n"
        
        for col in columns:
            schema_info += f"  - {col[0]} ({col[1]})\n"

    cur.close()
    conn.close()
    
    return schema_info

def get_ai_response(question, schema_info):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = (
        f"Use the following Snowflake schema details:\n"
        f"{schema_info}\n"
        f"Now, convert the user's question into a SQL query:\n"
        f"\"{question}\""
    )

    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=4096,
        top_p=0.95,
        stream=False,
    )

    full_response = completion.choices[0].message.content
    clean_response = re.sub(r"<think>.*?</think>", "", full_response, flags=re.DOTALL).strip()

    return clean_response

def upload_to_s3(df, bucket_name, s3_path):
    try:
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        
        s3_client.put_object(Body=csv_buffer.getvalue(), Bucket=bucket_name, Key=s3_path)
        st.success(f"📥 File successfully uploaded to S3 at {bucket_name}/{s3_path}")
    except NoCredentialsError:
        st.error("❌ No credentials available to upload to S3!")
    except Exception as e:
        st.error(f"❌ Error uploading file: {e}")

question = st.text_input("💬 Ask a question about your Snowflake data:")

if st.button("Get SQL Query and Results"):
    if question:
        try:
            schema_info = get_schema_info(db_choice)
            ai_response = get_ai_response(question, schema_info)

            st.subheader("🛠️ AI-Generated SQL Query:")
            
            sql_match = re.search(r"```sql\n(.*?)\n```", ai_response, re.DOTALL)
            sql_query = sql_match.group(1).strip() if sql_match else ai_response.strip()

            st.code(sql_query)

            try:
                conn = get_snowflake_connection(db_choice)
                cur = conn.cursor()
                
                cur.execute(sql_query)
                rows = cur.fetchall()
                
                columns = [desc[0] for desc in cur.description]
                df = pd.DataFrame(rows, columns=columns)

                st.subheader("📊 Query Results:")
                st.dataframe(df)

                st.session_state.df = df

                cur.close()
                conn.close()

            except Exception as e:
                st.error(f"❌ Snowflake Error: {e}")

        except Exception as e:
            st.error(f"❌ Failed to generate a valid SQL query: {e}")
    else:
        st.warning("⚠️ Please enter a question.")

if st.button("Upload Results to S3"):
    if 'df' in st.session_state:
        df = st.session_state.df
        bucket_name = os.getenv("S3_BUCKET_NAME")
        s3_path = "output_folder/data_export.csv"
        
        upload_to_s3(df, bucket_name, s3_path)
    else:
        st.warning("⚠️ Please get the results first by asking a question.")
