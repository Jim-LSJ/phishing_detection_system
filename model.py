import lightgbm as lgb

def load_model():
    return lgb.Booster(model_file='Weight/mix60_0')

def lgbm_pred(df, gbm):
    pred_x = df[['Cookies', 'httponly', 'secure', 'session', 'session & httponly',
                'Tags', 'No-class Tags', 'class Tags', 
                'div', 'img', 'iframe', 'a', 'form', 'input', 
                'script', 'internal_script', 'external_script'
                ]]

    pred_y = gbm.predict(pred_x, num_iteration=gbm.best_iteration)
    pred_y = np.where(pred_y > 0.5, 1, 0)

    print("Finish lightgbm predict")
    return pred_y