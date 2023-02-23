import os
import pandas as pd

# setting object
import config as c

# -----------------------------------------------
# Optimization function
# -----------------------------------------------
def objective(trial): # trial is optuna function, for suggest params

    # parameter
    params1 = trial.suggest_uniform(c.params["params1"]["idx"],
                                    c.params["params1"]["min"],
                                    c.params["params1"]["max"])
    params2 = trial.suggest_uniform(c.params["params2"]["idx"],
                                    c.params["params2"]["min"],
                                    c.params["params2"]["max"])
    params3 = trial.suggest_uniform(c.params["params3"]["idx"],
                                    c.params["params3"]["min"],
                                    c.params["params3"]["max"])

    # return target values
    X = c.return_X(c.BaseX, "under_calculating", c.X_idx, c.params, params_idx="params1", update_value=params1)
    X = c.return_X(X, "under_calculating", c.X_idx, c.params, params_idx="params2", update_value=params2)
    X = c.return_X(X, "last", c.X_idx, c.params, params_idx="params3", update_value=params3)

    y1 = c.model1.predict(X)[0]
    y2 = c.model2.predict(X)[0]

    return y1, y2