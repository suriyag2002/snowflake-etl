### ✅ `README.md`

## 🎥 Demo Video



https://github.com/user-attachments/assets/6e4cddce-deff-4d49-b403-9783179727c8




## 🚀 **Snowflake ETL Pipeline with AI-Powered Query Generation and S3 Integration**

This project is a **Streamlit-based web application** that allows users to:
- Ask **natural language questions** about their Snowflake data.
- Generate **SQL queries** using **Groq AI**.
- Execute the SQL queries in **Snowflake**.
- Display the results in a **DataFrame**.
- Export the results as a CSV file and **upload them to S3**.

---

### ⚙️ **Features**
- **Natural Language to SQL:** AI-powered query generation using Groq.
- **Dynamic Snowflake Schema Detection:** Automatically fetches table and column details.
- **Real-time Query Execution:** Runs SQL queries and displays results.
- **S3 Integration:** Uploads query results as CSV files to Amazon S3.
- **Environment Variables:** Stores sensitive credentials in a `.env` file.

---

### 🛠️ **Tech Stack**
- **Backend:** Python, Snowflake, Groq AI, Boto3 (AWS S3)
- **Frontend:** Streamlit
- **Cloud Storage:** Amazon S3
- **AI Model:** Groq (DeepSeek-R1 Distill Llama 70B)

---

### 📦 **Installation**

1. **Clone the Repository**
bash

git clone https://github.com/suriyag2002/snowflake-etl.git
cd snowflake-etl


2. **Create a virtual environment**
bash

python -m venv venv

source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows


3. **Install dependencies**
bash
pip install -r requirements.txt

4. **Set Up Environment Variables**
- Create a `.env` file in the project directory and add your credentials:

GROQ_API_KEY=YOUR_GROQ_KEY
SNOWFLAKE_USER=YOUR_USER
SNOWFLAKE_PASSWORD=YOUR_PASSWORD
SNOWFLAKE_ACCOUNT=YOUR_ACCOUNT
AWS_ACCESS_KEY=YOUR_AWS_ACCESS_KEY
AWS_SECRET_KEY=YOUR_AWS_SECRET_KEY
AWS_REGION=YOUR_AWS_REGION

---

### 🚀 **Run the Application**
Start the Streamlit app:
bash

streamlit run app.py


### 🛠️ **Usage**
1. Select the **Snowflake database** from the dropdown.
2. Enter your **natural language question**.
3. Click **"Get SQL Query and Results"** to generate the SQL query and view the results.
4. To export the results, click **"Upload Results to S3"**.

---

### ⚠️ **Environment Variables and Secrets**
- Ensure you never push sensitive credentials (like Snowflake or AWS keys) to GitHub.
- Use the `.env` file and `gitignore` to keep your secrets safe.

---

### 🔥 **Deployment**
You can deploy this app on **Render** or **Railway**:
1. Create a new **Python + Web Service** on Render.
2. Add the environment variables in the Render dashboard.
3. Deploy the app with Streamlit commands.

---

### 📚 **Folder Structure**
```
/aws-etl-app
 ├── .env                # Environment variables
 ├── app.py              # Streamlit app
 ├── requirements.txt    # Python dependencies
 ├── README.md           # Project documentation
 └── .gitignore          # Ignore sensitive files
```

---

### 🚀 **Future Enhancements**
- Add **error handling** for SQL syntax errors and Snowflake exceptions.
- Add **pagination** for large query results.
- Enhance the **UI/UX** with interactive filters.
- Include **data visualization** using Plotly or Matplotlib.

---

### 🛠️ **Contributors**
- **SURIYA** – Data Engineer

