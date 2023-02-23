import os
import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
import pickle

# -----------------------------------------------
# Base function
# -----------------------------------------------
def loadmodel(filepath):
    with open(filepath, "rb") as f:
        model = pickle.load(f)
    return model

def dataset(datasetpath):
    df = pd.read_csv(datasetpath)

    # X
    X = df.drop(labels=["volatile acidity", "citric acid", "quality"], axis=1)

    # base line value
    BaseX = X.mean().values
    X_idx = X.mean().index

    # params
    params = {
            "params1":{
                "idx":'fixed acidity',
                "min":X['fixed acidity'].min(),
                "max":X['fixed acidity'].max()
            },
            "params2":{
                "idx":'residual sugar',
                "min":X['residual sugar'].min(),
                "max":X['residual sugar'].max()
            },
            "params3":{
                "idx":'free sulfur dioxide',
                "min":X['free sulfur dioxide'].min(),
                "max":X['free sulfur dioxide'].max()
            },
        }

    return BaseX, X_idx, params

def GMM_dataset(datasetpath):

    df = pd.read_csv(datasetpath)

    # X
    X = df[['fixed acidity', 'residual sugar', 'free sulfur dioxide']]

    # standard scaler
    sc = StandardScaler()
    X_std = sc.fit_transform(X)

    return X_std, sc

def return_X(X, timing, X_idx, params, params_idx, update_value):

    # update value
    X[X_idx==params[params_idx]["idx"]] = update_value

    # return by timing
    if timing=="under_calculating":
        return X
    elif timing=="last":
        # reshape
        return X.reshape(1,-1)

# -----------------------------------------------
# GMM model
# -----------------------------------------------

class GMM_model:

    def __init__(self, X_std, sc):
        # dataset
        self.X = X_std
        self.sc = sc

    def fit_model(self, max_n_components):
        n_comps = np.arange(1, max_n_components+1)
        self.gmm_models = []
        self.bic_list = []
        # calc each BIC
        for i in n_comps:
            # fit model
            gmm = GaussianMixture(n_components=i, max_iter=30, random_state=10)
            gmm.fit(self.X)
            # calc bic
            bic = gmm.bic(self.X)
            # append to list
            self.gmm_models.append(gmm)
            self.bic_list.append(bic)
        # change to numpy array bic_list
        self.bic_list = np.array(self.bic_list)

        # select best bic
        print(f"Best n_components = {np.argmin(self.bic_list)}")
        self.gmm = self.gmm_models[np.argmin(self.bic_list)]


# -----------------------------------------------
# Initial objects
# -----------------------------------------------

print("Start Initial calculation")
print("")
print(" - Load dataset")
datasetpath = r"*.csv"
print(" - Preprocessing dataset")
BaseX, X_idx, params = dataset(datasetpath=datasetpath)
print(" - Load leared models")
# load model test
model1 = loadmodel(filepath=os.path.join(r"*",
                                              "model1.pickle"))
model2 = loadmodel(filepath=os.path.join(r"*",
                                              "model2.pickle"))
print("")


print("Start pre training GMM model")
# for GMM dataset
print(" - Load dataset")
X_std, sc = GMM_dataset(datasetpath=datasetpath)
print(" - Start learning Gaussian mixture model")
print(" - Calculating best n_components by bic")
gmm = GMM_model(X_std, sc)
gmm.fit_model(max_n_components=10)