# Real Estate Portfolio Optimization in Jabodetabek

<img width="968" height="412" alt="Screenshot 2025-11-21 151927" src="https://github.com/user-attachments/assets/1c79b564-60e6-4421-9fd7-44afb40cc524" />

This project applies machine learning and dynamic programming to forecast and optimize real estate investments in the Jabodetabek region. It combines XGBoost-based prediction models for rent and property appreciation with a knapsack optimization algorithm to maximize Net Present Value (NPV) under a fixed budget.
(NOTE: This project is for academic and educational purposes. Not intended as financial advice or investment recommendation.)

## 📁 Project Structure

```
STIMA-MAKALAH-ANALYSIS/
├── cleaned_datasets/             
├── raw_datasets/               
├── .gitignore                    
├── algorithms.py                 
├── data_analysis.ipynb          
├── data_modelling.ipynb         
├── data_preparation.ipynb       
├── main.py                       
├── rumah123_2025_sale_modelled.csv  
├── README.markdown               
├── requirements.txt              
```


## 🚀 How to Run

1. **Clone the repository**

```bash
git clone https://github.com/your-username/STIMA-MAKALAH-ANALYSIS.git
cd STIMA-MAKALAH-ANALYSIS
```

2. **Set up your environment**

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

3. **Run the main optimization**

```bash
python main.py
```

> The script will load the dataset, evaluate different portfolio selection algorithms (Dynamic Programming, Greedy, Brute Force), and output performance summaries.


## 📊 Features

* **Forecasting**

  * Sale Price (2025): trained using historical property features
  * Rent Estimate (2025): trained from Rumah123 rental listings
  * Capital Gain (CAGR) estimation using predicted 2023–2025 values

* **Investment Optimization**

  * Dynamic Programming-based exact knapsack solver
  * Greedy heuristic for fast approximations
  * Brute-force benchmark (small test cases)

* **Evaluation**

  * Comparative performance across 1000 trials
  * Greedy vs. DP accuracy rate
  * Simulation of projected growth (future value)


## 🛠️ Dependencies

See `requirements.txt` for the full list. Key packages:

* `xgboost`
* `pandas`, `numpy`
* `matplotlib`, `seaborn`
* `scikit-learn`



## 🙏 Acknowledgments

* Rumah123 for publicly accessible listings
* Kaggle dataset: [Daftar Harga Rumah Jabodetabek](https://www.kaggle.com/datasets/nafisbarizki/daftar-harga-rumah-jabodetabek)
* IF2211 Algorithm Strategies course at Institut Teknologi Bandung



## 🧑‍💻 Author

| Name           | NIM      | Class  |
|----------------|----------|--------|
| Asybel Bintang | 15223011 | K1     |
