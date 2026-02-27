from entsoe import EntsoePandasClient
import pandas as pd

API_KEY = "***REMOVED***"

client = EntsoePandasClient(api_key=API_KEY)

start = pd.Timestamp('20250101', tz='Europe/Brussels')
end = pd.Timestamp.now(tz='Europe/Brussels') - pd.Timedelta(days=1)

fr_bidding_zone = 'FR'
no_bidding_zones_all = ['NO_1', 'NO_1A', 'NO_2', 'NO_2_NSL', 'NO_2A', 'NO_3', 'NO_4', 'NO_5']
no_bidding_zones_skip = ['NO_1A', 'NO_2A']

fr_all_borders_outbound = client.query_physical_crossborder_allborders(fr_bidding_zone, start, end, export=True, per_hour=True)
fr_all_borders_inbound = client.query_physical_crossborder_allborders(fr_bidding_zone, start, end, export=False, per_hour=True)

no_outbound = {}
no_inbound = {}

for zone in no_bidding_zones_all:
    try:
        no_outbound[zone] = client.query_physical_crossborder_allborders(zone, start, end, export=True, per_hour=True)
    except KeyError:
        print(f"{zone} outbound not recognized, skipping")
        
    try:
        no_inbound[zone] = client.query_physical_crossborder_allborders(zone, start, end, export=False, per_hour=True)
    except KeyError:
        print(f"{zone} inbound not recognized, skipping")
