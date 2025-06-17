import owslib
import geopandas as gpd
from owslib.csw import CatalogueServiceWeb
from shapely.geometry import Polygon

def csw2gpkg(url, filename):
    titles = []
    geometries = []
    metadata_id = []
    csw = CatalogueServiceWeb(url)
    csw.getrecords2(maxrecords=10)
    total_records = csw.results['matches']
    start_position = 1
    max_records_per_request = 100
    while start_position <= total_records:
        csw.getrecords2(maxrecords=max_records_per_request, startposition=start_position)
        print(f"Record: {start_position}")
        for rec in csw.records:
            try:
                polygon = Polygon([
                    (csw.records[rec].bbox.minx, csw.records[rec].bbox.miny),
                    (csw.records[rec].bbox.minx, csw.records[rec].bbox.maxy),
                    (csw.records[rec].bbox.maxx, csw.records[rec].bbox.maxy),
                    (csw.records[rec].bbox.maxx, csw.records[rec].bbox.miny),
                    (csw.records[rec].bbox.minx, csw.records[rec].bbox.miny),
                    (csw.records[rec].bbox.minx, csw.records[rec].bbox.miny)
                ])
                titles.append(csw.records[rec].title)
                geometries.append(polygon)
                metadata_id.append(rec)
            except:
                print(f"Record {rec} has no bounding box")
                titles.append(csw.records[rec].title)
                geometries.append(None)
                metadata_id.append(rec)
        start_position += max_records_per_request
    gdf = gpd.GeoDataFrame({'title': titles, 'geometry': geometries, 'metadata_id': metadata_id}, crs="EPSG:4326")
    gdf.to_file(filename, driver='GPKG')
    return None

if __name__ == "__main__":
    print(csw2gpkg("http://bdgex.eb.mil.br/csw", "bdgex.gpkg"))