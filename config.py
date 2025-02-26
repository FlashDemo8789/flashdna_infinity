import os

MONGO_URI = os.getenv("MONGO_URI","mongodb://localhost:27017/flash_dna")

XGB_PARAMS = {
    "n_estimators": 100,
    "max_depth": 5,
    "learning_rate": 0.1,
    "use_label_encoder": False,
    "eval_metric": "logloss",
    "random_state": 42
}

ENV = os.getenv("ENV","dev")