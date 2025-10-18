import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import json

# Load data
df = pd.read_csv('Telco-Customer-Churn.csv')

# Data preprocessing
# Convert TotalCharges to numeric
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

# Fill missing values
df["TotalCharges"].fillna(df["TotalCharges"].median(), inplace=True)

# Convert categorical variables
df['gender'] = df['gender'].map({'Female': 0, 'Male': 1})
df['Partner'] = df['Partner'].map({'No': 0, 'Yes': 1})
df['Dependents'] = df['Dependents'].map({'No': 0, 'Yes': 1})
df['PhoneService'] = df['PhoneService'].map({'No': 0, 'Yes': 1})
df['PaperlessBilling'] = df['PaperlessBilling'].map({'No': 0, 'Yes': 1})
df['Churn'] = df['Churn'].map({'No': 0, 'Yes': 1})

# One-hot encoding for categorical variables
categorical_columns = ['InternetService', 'Contract', 'PaymentMethod', 'MultipleLines', 'OnlineSecurity',
                      'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
df_encoded = pd.get_dummies(df, columns=categorical_columns)

# Select features for model
feature_columns = [col for col in df_encoded.columns if col != 'Churn' and col != 'customerID']

# Save feature columns for later use
with open('feature_columns.json', 'w') as f:
    json.dump(feature_columns, f)

# Prepare features and target
X = df_encoded[feature_columns]
y = df_encoded['Churn']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save scaler for later use
import pickle
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# Build the model
model = Sequential([
    Dense(128, activation='relu', input_shape=(len(feature_columns),)),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train the model
history = model.fit(X_train_scaled, y_train,
                    epochs=5,
                    batch_size=32,
                    validation_split=0.2,
                    verbose=1)

# Evaluate the model
y_pred_proba = model.predict(X_test_scaled)
y_pred = (y_pred_proba > 0.5).astype(int)

# Calculate metrics
test_loss, test_accuracy = model.evaluate(X_test_scaled, y_test, verbose=0)
roc_auc = roc_auc_score(y_test, y_pred_proba)

print(f'\nTest Accuracy: {test_accuracy:.4f}')
print(f'ROC-AUC:       {roc_auc:.4f}\n')

# Print classification report
print('Classification report:')
print(classification_report(y_test, y_pred))

# Print confusion matrix
print('Confusion matrix:\n', confusion_matrix(y_test, y_pred))

# Save the model
model.save('churn_model.h5')

print("\n✅ Saved files: churn_model.h5, scaler.pkl, feature_columns.json")