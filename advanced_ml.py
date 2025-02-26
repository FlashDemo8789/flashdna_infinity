import xgboost as xgb
import numpy as np
from intangible_llm import compute_intangible_llm
from domain_expansions import apply_domain_expansions
from team_moat import compute_team_depth_score, compute_moat_score
from constants import NAMED_METRICS_50

def build_feature_vector(doc: dict)-> np.ndarray:
    base_50= [float(doc.get(m,0.0)) for m in doc.get("named_metrics_50",NAMED_METRICS_50[:5])]
    expansions= apply_domain_expansions(doc)
    intangible_val= compute_intangible_llm(doc)
    team_val= compute_team_depth_score(doc)
    moat_val= compute_moat_score(doc)
    ex_vals= list(expansions.values())
    arr= base_50 + ex_vals + [intangible_val, team_val, moat_val]
    return np.array(arr,dtype=float)

def predict_success(doc: dict, xgb_model)-> float:
    fv= build_feature_vector(doc).reshape(1,-1)
    prob= xgb_model.predict_proba(fv)[0][1]*100
    return prob