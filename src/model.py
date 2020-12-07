import pandas as pd
import numpy as np
import zipfile
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import mean_squared_error, confusion_matrix, precision_score, recall_score, roc_curve, auc, roc_auc_score, f1_score
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV
import helper_functions

df = pd.read_csv('data/food_insecurity.csv')
df.set_index('caseid2019', inplace=True)
df_analysis = df.copy()
df_analysis.dropna(inplace=True)
df_analysis.info()

y = df_analysis.pop('Applied for SNAP')
y_alt = df_analysis.pop('Applied SNAP but not received')
X = df_analysis

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, stratify=y, random_state=1)


# Decision Tree
dt = DecisionTreeClassifier(random_state=0)
dt.fit(X_train, y_train)
y_predict = dt.predict(X_test)

print("Decision Tree")
print("score:", dt.score(X_test, y_test))
print("confusion matrix:")
print(confusion_matrix(y_test, y_predict))
print("precision:", precision_score(y_test, y_predict))
print("recall:", recall_score(y_test, y_predict))
print("f1:", f1_score(y_test, y_predict))
dt_f1 = f1_score(y_test, y_predict)

# Random Forest
rf1 = RandomForestClassifier(random_state=0)
rf1.fit(X_train, y_train)
y_predict = rf1.predict(X_test)

print("score:", rf1.score(X_test, y_test))
print("confusion matrix:")
print(confusion_matrix(y_test, y_predict))
print("precision:", precision_score(y_test, y_predict))
print("recall:", recall_score(y_test, y_predict))
print("f1:", f1_score(y_test, y_predict))


#Random Forest Grid Search Tuning
random_forest_grid = {'max_depth': [2, 4, None],
                      'max_features': ['sqrt', 'log2', None],
                      'min_samples_split': [2, 4],
                      'min_samples_leaf': [1, 2, 4],
                      'bootstrap': [True, False],
                      'oob_score': [True, False],
                      'n_estimators': [20, 30, 40, 50],
                      'class_weight': ['balanced', None],
                      'random_state': [1]
                     }
rf_best_params, rf_best_model, rf_best_score = gridsearch_with_output(RandomForestClassifier(), 
                                                                      random_forest_grid, 
                                                                      score,
                                                                      X_train, y_train)

rf_best = rf_best_model.fit(X_train, y_train)
y_predict = rf_best.predict(X_test)

print("score:", rf_best.score(X_test, y_test))
print("confusion matrix:")
print(confusion_matrix(y_test, y_predict))
print("precision:", precision_score(y_test, y_predict))
print("recall:", recall_score(y_test, y_predict))
print("f1:", f1_score(y_test, y_predict))
rfbest_f1 = f1_score(y_test, y_predict)

importances = rf_best.feature_importances_
indices = np.argsort(importances)[::-1]
features = list(df_analysis.columns[indices])
print("Feature ranking:")
for f in range(n):
    print("%d. %s (%f)" % (f + 1, features[f], importances[indices[f]]))

# Plot the feature importances of the forest
fig, ax = plt.subplots(figsize=(10, 8))
ax.barh(range(n), importances[indices][:n], color="r", align="center")
ax.set_yticks(range(n))
ax.set_yticklabels(features[:n])
ax.set_ylim([-1, n])
ax.set_xlabeal("Importance")
ax.set_title("Random Forest Classifier Feature Importances")
fig.savefig('images/rf_feature_importance.png', bbox_inches = "tight")

#Gradient Boosting
gb = GradientBoostingClassifier(random_state=1)
gb.fit(X_train, y_train)
y_predict = gb.predict(X_test)

print("score:", gb.score(X_test, y_test))
print("confusion matrix:")
print(confusion_matrix(y_test, y_predict))
print("precision:", precision_score(y_test, y_predict))
print("recall:", recall_score(y_test, y_predict))
print("f1:", f1_score(y_test, y_predict))

#Plot learning rate and boosting stages on F1 score
gb_1 = GradientBoostingClassifier(learning_rate=.1, random_state=1)
gb_2 = GradientBoostingClassifier(learning_rate=.25, random_state=1)
gb_3 = GradientBoostingClassifier(learning_rate=.5, random_state=1)
gb_4 = GradientBoostingClassifier(learning_rate=.75, random_state=1)
gb_5 = GradientBoostingClassifier(learning_rate=1, random_state=1)

stage_f1score_plot(gb_1, X_train, y_train, X_test, y_test, 'red')
#stage_f1score_plot(gb_2, X_train, y_train, X_test, y_test, 'orange')
stage_f1score_plot(gb_3, X_train, y_train, X_test, y_test, 'blue')
stage_f1score_plot(gb_4, X_train, y_train, X_test, y_test, 'green')
#stage_f1score_plot(gb_5, X_train, y_train, X_test, y_test, 'green')

plt.axhline(rf_best_score, alpha = 0.7, c = 'y', lw=3, ls='-.', label = 
                                                         'Random Forest Train')
plt.axhline(f1_score(y_test, y_predict), alpha = 0.7, c = 'black', lw=3, ls='-.', label = 
                                                        'Random Forest Test')

plt.title('', fontsize=16, fontweight='bold')
plt.legend(loc='lower right', fontsize=7)
plt.savefig('images/gb_bosstingstages.png', bbox_inches = "tight")

#Gradient Boosting Grid Search 
gb_grid = {'max_depth': [2, 4, None],
           'max_features': ['sqrt', 'log2', None],
           'min_samples_split': [2, 4, None],
           'min_samples_leaf': [1, 2, 4, None],
           'n_estimators': [20, 30, 40, 50, 60],
           'learning_rate': [.5, .6, .7],
           'random_state': [1]
                     }

gb_best_params, gb_best_model, gb_best_score = gridsearch_with_output(GradientBoostingClassifier(), 
                                                           gb_grid, 
                                                           'f1',
                                                           X_train, y_train)

gb_best = gb_best_model.fit(X_train, y_train)
y_predict = gb_best.predict(X_test)

print("score:", gb_best.score(X_test, y_test))
print("confusion matrix:")
print(confusion_matrix(y_test, y_predict))
print("precision:", precision_score(y_test, y_predict))
print("recall:", recall_score(y_test, y_predict))
print("f1:", f1_score(y_test, y_predict))

#Score improvement 
improvement = (rfbest_f1 - dt_f1) / dt_f1
print(f"%improvement: {improvement*100}%")