# AI-Enabled Recommendation System

## 📌 Project Description
This project is an **AI-Enabled Recommendation System** developed using **Python**.  
The system recommends products to users based on their interaction history using a collaborative filtering approach.

The application is implemented using **Streamlit**, where both the recommendation logic and the user interface are handled within a single application.

---

## 🛠️ Technologies Used
- Python  
- Streamlit  
- Pandas  
- NumPy  
- Scikit-learn  

---

## 📂 Project Structure
AI-Enabled-Recommendation-System/
│
├── backend/
│ └── recommender/
│ └── main.py
│
├── data/
│ └── cleaned_data.csv
│
├── evaluation/
│ └── metrics.py
│
├── app.py
├── requirements.txt
├── runtime.txt
│
├── Agile_Template_v0.1.xls
├── Defect_Tracker Template_v0.1.xlsx
├── Unit_Test_Plan_v0.1.xlsx
│
└── README.md

---

## ⚙️ How the System Works
1. User selects a **User ID** in the Streamlit interface  
2. The application loads the dataset and processes user interaction data  
3. Recommendation logic is applied using collaborative filtering  
4. Top product recommendations are generated  
5. Results are displayed directly in the Streamlit UI  

---

## ▶️ How to Run the Project

### Step 1: Clone the repository
```bash
git clone https://github.com/sritejreddy04/AI-Enabled-Recommendation-System.git
cd AI-Enabled-Recommendation-System

Step 2: Install dependencies
pip install -r requirements.txt

Step 3: Run the application
streamlit run app.py

The application will open in the browser at:
http://localhost:8501
👤 Author

Jinne Sri Teja Reddy
✅ Project Status

Project implementation completed

Code pushed to GitHub

Documentation added
