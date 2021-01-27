import pandas as pd

def predict(cleaned_json_df, model):

    X_new_json = cleaned_json_df.values

    y_pred_new = model.predict(X_new_json)

    # to round these number to make it readable ini html
    for i, y_pred in enumerate(y_pred_new):
        y_pred_new[i] = round(y_pred)

    return y_pred_new





