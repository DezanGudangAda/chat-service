from dataclasses import dataclass


@dataclass
class DatabaseConfiguration:
    host: str
    port: int
    username: str
    db: str
    password: str


@dataclass
class GetStreamConfiguration:
    secret: str
    api_key: str


@dataclass
class ExternalServiceConfiguration:
    gada_marketplace: str


@dataclass
class Configuration:
    database: DatabaseConfiguration
    get_stream: GetStreamConfiguration
    external_service: ExternalServiceConfiguration
