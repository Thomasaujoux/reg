import pickle
import re
from pathlib import Path


def get_score(df, model, weight_pos = 1, weight_model = 1, weight_popu=1):

    prediction = model.predict(df)
    return prediction