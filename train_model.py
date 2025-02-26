import xgboost as xgb
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from config import XGB_PARAMS
from advanced_ml import build_feature_vector

def load_training_data():
    data_docs= [
      {"outcome":"pass","named_metrics_50":["monthly_revenue","user_growth_rate","burn_rate","churn_rate","ltv_cac_ratio"],
       "monthly_revenue":50000,"user_growth_rate":0.1,"burn_rate":30000,"churn_rate":0.05,"ltv_cac_ratio":3.0,
       "founder_exits":1,"founder_domain_exp_yrs":5,"pitch_deck_text":"We overcame synergy BFS by HPC + LLM."},
      {"outcome":"fail","named_metrics_50":["monthly_revenue","user_growth_rate","burn_rate","churn_rate","ltv_cac_ratio"],
       "monthly_revenue":8000,"user_growth_rate":0.02,"burn_rate":12000,"churn_rate":0.15,"ltv_cac_ratio":1.2,
       "founder_exits":0,"founder_domain_exp_yrs":2,"pitch_deck_text":"fear meltdown BFS synergy pivot..."}
    ]
    X_list, y_list= [],[]
    for doc in data_docs:
        fv= build_feature_vector(doc)
        X_list.append(fv)
        y_list.append(1 if doc["outcome"]=="pass" else 0)
    return np.array(X_list), np.array(y_list,dtype=int)

def train_model_xgb():
    X,y= load_training_data()
    X_train,X_test,y_train,y_test= train_test_split(X,y,test_size=0.2,random_state=42)
    model= xgb.XGBClassifier(**XGB_PARAMS)
    model.fit(X_train,y_train)
    tr= model.score(X_train,y_train)
    te= model.score(X_test,y_test)
    print(f"Train acc={tr:.2f}, test acc={te:.2f}")
    with open("model_xgb.pkl","wb") as f:
        pickle.dump(model,f)
    print("Saved model_xgb.pkl")

if __name__=="__main__":
    train_model_xgb()