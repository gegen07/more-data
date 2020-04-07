import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import json
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk

import enrichment.parser as models
import enrichment.models as models
from enrichment.enricher.elasticsearch_connector import IndexHandler


import enrichment.utils.processing as processing

host = 'localhost'

ELK_MAPS_DIR = "../elk-maps/"
MAPPING_DIR = ELK_MAPS_DIR + "mappings/"

DATASETS_DIR = "../../datasets/"

APP_DATA = DATASETS_DIR + "ranking_apps.csv"
USER_DATA = DATASETS_DIR + "user_profile_17092019.json"
CENSUS_DATA = DATASETS_DIR + "df_census_2010.csv"

LOCALS_DIR = DATASETS_DIR + "Locais_OSM/geojson/"
SETORES_DIR = DATASETS_DIR + "setores/"

CIDADES_DIR = DATASETS_DIR + "cidades_info_polygon.csv"

MAPPING_LOCAL_FILE = MAPPING_DIR + "points-interests/locals.json"

def read_json(file):
    with open(file, "r") as f:
        return json.loads(f.read())

def bulk_user(client):
    user = models.Data(data_file=USER_DATA, parser_func=parser.parsers.parse_user, data_type="json")
    query_user = models.Query(client, "users", "user")
    query_user.load_index(user.parse)

def bulk_app(client):
    app = models.Data(data_file=APP_DATA, parser_func=parser.parsers.csv_generator, data_type="csv")
    query_app = models.Query(client, "apps", "app")
    query_app.load_index(app.parse)

def bulk_locals(client):
    query = models.Query(client, "locals", "local")

    mapping = read_json(MAPPING_LOCAL_FILE)

    query.create_index(mapping)

    import glob

    dir = LOCALS_DIR + "*.geojson"
    files = glob.glob(dir)

    for file in files:
        locals = models.Data(data_file=file, parser_func=parser.parsers.parse_local_geojson, data_type="json")
        query.load_index(parser=locals.parse, streaming=True)

def bulk_census_data(client):
    census = models.Data(data_file=CENSUS_DATA, parser_func=parser.parsers.parse_census, data_type="csv")
    query = models.Query(client, "census", "sector")
    query.load_index(census.parse)

def bulk_h3_sectors_data(client, data_type):

    import glob
    dir = SETORES_DIR+"*."+data_type
    files = glob.glob(dir)

    for file in files:
        print(file)
        sector = models.Data(data_file=file, parser_func=parser.parsers.parse_setores, data_type="csv")
        query = models.Query(client, "sectors", "h3_sector")
        query.load_index(sector.parse)

if __name__ == '__main__':
    es = Elasticsearch(
        hosts=[{'host': host, 'port': 9200}]
    )

    # bulk_census_data(es)
    bulk_user(es)
    # bulk_locals(es)