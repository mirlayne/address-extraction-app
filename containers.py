import logging.config

from dependency_injector import containers, providers

from infrastructure.mongo_api import MongoAPI as MongoAPI
from use_cases.metadata_extraction import MetadataExtraction as MetadataExtraction


class Container(containers.DeclarativeContainer):
    '''
    Containers for the dependency injection
    '''
    config = providers.Configuration()

    logging = providers.Resource(
        logging.config.fileConfig,
        fname='logging.ini',
    )

    # Gateways

    mongodb_client = providers.Singleton(
        mongodb_url=config.mongodb_url
    )

    tika_client = providers.Singleton(
        tika_server=config.tika_server
    )

    # Services

    metadata_extraction = providers.Factory(
        MetadataExtraction,
        tika_server=tika_client
    )

    mongodb_api = providers.Factory(
        MongoAPI,
        mongodb_url=mongodb_client
    )
