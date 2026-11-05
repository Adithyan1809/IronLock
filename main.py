from asyncio.log import logger
import sys
from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.components.data_transformation import DataTransformation
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig , DataValidationConfig , DataTransformationConfig
from NetworkSecurity.entity.artifact_entity import DataIngestionArtifact

if __name__=='__main__':
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        
        logging.info("Initiating the data ingestion process")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)
        logging.info("Data ingestion process completed")
        
        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        
        logging.info("Initiating the data validation process")
        data_validation=DataValidation(dataingestionartifact,data_validation_config)
        data_validation_artifact=data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info("Data validation process completed")

        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        
        logging.info("Initiating the data transformation process")
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)

        data_transformation_artifact=data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("Data transformation process completed")
    except Exception as e:
           raise NetworkSecurityException(e,sys)