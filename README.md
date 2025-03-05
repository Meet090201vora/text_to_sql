
# FastAPI SQL Query Agent

This project integrates **LangChain** with **FastAPI** to create a chatbot agent that queries a **PostgreSQL** database using **OpenAI's GPT-4o-mini**.

## Features
- Uses **GPT-4o-mini** for natural language SQL queries.
- Streams responses for a faster, interactive experience.
- Built with **FastAPI** for efficient API handling.
- Connects to a **PostgreSQL** database.

---

## **Installation**
### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### **2. Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Set Up Environment Variables**
Create a `.env` file in the root directory and add:
```ini
OPENAI_API_KEY=your-openai-api-key
POSTGRES_PASSWORD=your-postgres-password
```

Edit `config.py` to define:
```python
postgres_user = "your_username"
postgres_database = "your_database"
```

---

## **Usage**
### **Run the FastAPI Server**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
or (if command throws error)
```
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The server will start at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### **Test the API**
#### **POST `/query/`**
**Request:**
```json
{
  "query": "Which country's customers spent the most?"
}
```
**Using cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/query/" -H "Content-Type: application/json" -d '{"query": "Which country\'s customers spent the most?"}'
```

**Response (Streamed Output):**
```
USA
----
```

---

**Use the UI parallely**
Once the API is up and running. you can create a different terminal and use the following command to use the API
```
streamlit run app.py
```

---

## **License**
MIT License © 2025 Meet Vora

---

## **Contributors**
- **Meet Vora** - [GitHub](https://github.com/your-username)


---

### **Key Sections Covered:**
✅ **Installation Steps**  
✅ **Running the FastAPI Server**  
✅ **API Usage Example**  
✅ **Environment Setup**    

Let me know if you need modifications! 🚀
