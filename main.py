from asyncio.log import logger
import sys
from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig , DataValidationConfig
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
        data_validation=DataValidation(dataingestionartifact,data_validation_config)
        
        logging.info("Initiating the data validation process")
        data_validation_artifact=data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info("Data validation process completed")
    except Exception as e:
           raise NetworkSecurityException(e,sys)