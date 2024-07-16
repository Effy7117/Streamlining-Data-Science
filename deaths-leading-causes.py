import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import mlflow
import mlflow.sklearn
import psutil

# MLflow setup
mlflow.set_tracking_uri("/home/effy/mlruns")  
mlflow.set_experiment("deaths-leading-causes") 

def gather_system_metrics():
    # Gather system metrics using psutil
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    
    # Log system metrics to MLflow
    mlflow.log_metric("cpu_percent", cpu_percent)
    mlflow.log_metric("memory_percent", memory_percent)
    mlflow.log_metric("disk_percent", disk_percent)

def train_model():
    # Load dataset
    df = pd.read_excel('/home/effy/deaths-leading-causes-load.xlsx')

    X = df[['Cause_Encoded', 'Calendar Year', 'Ranking']]
    y = df['Total Deaths']

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize linear regression model
    model = LinearRegression()

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Log metrics and artifacts to MLflow
    with mlflow.start_run() as run:
        # Log system metrics
        gather_system_metrics()

        # Log parameters
        mlflow.log_param("data_size", len(df))
        mlflow.log_param("test_size", len(X_test))

        # Log metrics
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("r2", r2)

        # Log model
        mlflow.sklearn.log_model(model, "linear_regression_model")

        # Log evaluation results as a table
        results = pd.DataFrame({"Actual": y_test, "Predicted": y_pred})
        mlflow.log_table(data=results, artifact_file="predictions.json")

        # Log feature importances
        if hasattr(model, 'coef_'):
            coef_df = pd.DataFrame({"Feature": X.columns, "Coefficient": model.coef_})
            mlflow.log_table(data=coef_df, artifact_file="coefficients.json")

if __name__ == "__main__":
    train_model()

