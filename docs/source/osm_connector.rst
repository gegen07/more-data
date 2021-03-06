.. _osm_connector:

OSM Connector
=============
Examples
~~~~~~~~

This example implements the use of OSM Connector. The framework works with two manners to enrich data, one with radius around point and another without the radius. The first acts increasing the point resulting a polygon like a circle with this radius. The second doesn't buffer the point and verify if the point is within the polygons downloaded using OSM. You can use a file that you've already downloaded with restriction, you must have at least one column in your CSV: "geometry". 
The arguments `key` and `value` is available in `Map Features <https://wiki.openstreetmap.org/wiki/Map_Features>`_.  

.. code-block:: python
    
    # name of file: enrich-osm.py

    from moredata.enricher import EnricherBuilder, Enricher
    from moredata.enricher.osm_connector import OSMConnector
    from moredata.models.data import Data
    from moredata.parser import parse_document
    from moredata.utils.util import read_json_from_file, Converter

    user = Data(data_file=USER_DATA, parser_func=parse_document, data_type="json")

    osm_enricher = Enricher(connector=OSMConnector(key="amenity", value="hospital", place_name="São Paulo", radius=100, dict_keys=["points_of_interest"]))

    user_enriched = \
	  EnricherBuilder(user) \
	  .with_enrichment(osm_enricher) \
	  .get_result() 

    import moredata.utils.util as util

    util.write_json_generator_to_json("../../data/output/osm/amenity-cafe-mg", user_enriched, 100000) 

.. code-block:: bash
    
    $ python enrich-osm.py

OSM Connector
-------------

.. py:module:: moredata.enricher.osm.osm_places_connector

.. autoclass:: OSMPlacesConnector
    :members:

