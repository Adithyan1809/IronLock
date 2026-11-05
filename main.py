from asyncio.log import logger
import sys

from NetworkSecurity.components import data_ingestion
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from NetworkSecurity.entity.artifact_entity import DataIngestionArtifact

if __name__=='__main__':
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=data_ingestion.DataIngestion(dataingestionconfig)
        logging.info("Initiating the data ingestion process")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)
    except Exception as e:
           raise NetworkSecurityException(e,sys)