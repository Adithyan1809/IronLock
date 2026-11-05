
import os
import sys


import mlflow
import mlflow.sklearn
import dagshub

from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging

from NetworkSecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact
)

from NetworkSecurity.entity.config_entity import ModelTrainerConfig

from NetworkSecurity.utils.ml_utils.model.estimator import NetworkModel

from NetworkSecurity.utils.main_utils.utils import (
    save_object,
    load_object,
    load_numpy_array_data,
    evaluate_models
)

from NetworkSecurity.utils.ml_utils.metric.classification_metric import (
    get_classification_score
)

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)


# Initialize DagsHub and MLflow
dagshub.init(
    repo_owner='Adithyan1809',
    repo_name='IronLock',
    mlflow=True
)


class ModelTrainer:

    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
        data_transformation_artifact: DataTransformationArtifact
    ):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # MLflow Tracking
    def track_mlflow(
        self,
        best_model,
        classification_train_metric,
        classification_test_metric
    ):

        with mlflow.start_run():

            # Training Metrics
            mlflow.log_metric(
                "train_f1_score",
                classification_train_metric.f1_score
            )

            mlflow.log_metric(
                "train_precision",
                classification_train_metric.precision_score
            )

            mlflow.log_metric(
                "train_recall",
                classification_train_metric.recall_score
            )

            # Testing Metrics
            mlflow.log_metric(
                "test_f1_score",
                classification_test_metric.f1_score
            )

            mlflow.log_metric(
                "test_precision",
                classification_test_metric.precision_score
            )

            mlflow.log_metric(
                "test_recall",
                classification_test_metric.recall_score
            )

            # Log Model
            mlflow.sklearn.log_model(
                sk_model=best_model,
                name="model",
                skops_trusted_types=[
                    "sklearn.tree._tree.Tree"
                ]
            )

    # Model Training
    def train_model(self, X_train, y_train, X_test, y_test):

        models = {
            "Logistic Regression": LogisticRegression(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Random Forest": RandomForestClassifier(verbose=1),
            "AdaBoost": AdaBoostClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
        }

        params = {

            "Decision Tree": {
                'criterion': ['gini', 'entropy', 'log_loss'],
            },

            "Random Forest": {
                'n_estimators': [8, 16, 32, 128, 256]
            },

            "Gradient Boosting": {
                'learning_rate': [0.1, 0.01, 0.05, 0.001],
                'subsample': [0.6, 0.7, 0.75, 0.85, 0.9],
                'n_estimators': [8, 16, 32, 64, 128, 256]
            },

            "Logistic Regression": {},

            "AdaBoost": {
                'learning_rate': [0.1, 0.01, 0.001],
                'n_estimators': [8, 16, 32, 64, 128, 256]
            }
        }

        # Evaluate Models
        model_report: dict[str, float] = evaluate_models(
            X_train=X_train,
            y_train=y_train,
            X_test=X_test,
            y_test=y_test,
            models=models,
            param=params
        )

        # Select Best Model
        best_model_name = max(model_report, key=lambda name: model_report[name])        
        best_model_score = model_report[best_model_name]
        best_model = models[best_model_name]

        logging.info(f"Best Model Found: {best_model_name}")
        logging.info(f"Best Model Score: {best_model_score}")

        # Training Predictions
        y_train_pred = best_model.predict(X_train)

        classification_train_metric = get_classification_score(
            y_true=y_train,
            y_pred=y_train_pred
        )

        # Testing Predictions
        y_test_pred = best_model.predict(X_test)

        classification_test_metric = get_classification_score(
            y_true=y_test,
            y_pred=y_test_pred
        )

        # MLflow Tracking
        self.track_mlflow(
            best_model=best_model,
            classification_train_metric=classification_train_metric,
            classification_test_metric=classification_test_metric
        )

        # Load Preprocessor
        preprocessor = load_object(
            file_path=self.data_transformation_artifact.transformed_object_file_path
        )

        # Create Model Directory
        model_dir_path = os.path.dirname(
            self.model_trainer_config.trained_model_file_path
        )

        os.makedirs(model_dir_path, exist_ok=True)

        # Create Network Model
        network_model = NetworkModel(
            preprocessor=preprocessor,
            model=best_model
        )

        # Save Complete Model
        save_object(
            file_path=self.model_trainer_config.trained_model_file_path,
            obj=network_model
        )

        logging.info("Trained model saved successfully.")

        # Model Trainer Artifact
        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact=classification_train_metric,
            test_metric_artifact=classification_test_metric
        )

        return model_trainer_artifact

    # Initiate Model Trainer
    def initiate_model_trainer(self) -> ModelTrainerArtifact:

        try:

            train_file_path = (
                self.data_transformation_artifact.transformed_train_file_path
            )

            test_file_path = (
                self.data_transformation_artifact.transformed_test_file_path
            )

            # Load NumPy Arrays
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            # Split Features and Target
            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1]
            )

            # Train Model
            model_trainer_artifact = self.train_model(
                X_train=x_train,
                y_train=y_train,
                X_test=x_test,
                y_test=y_test
            )

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
