from entsoe import EntsoePandasClient
import pandas as pd

API_KEY = "***REMOVED***"

client = EntsoePandasClient(api_key=API_KEY)

start = pd.Timestamp('20250101', tz='Europe/Brussels')
end = pd.Timestamp.now(tz='Europe/Brussels') - pd.Timedelta(days=1)

def check_inbound_outbound_frames(key, outbound, inbound):
    checks = [ 
        outbound.columns.equals(inbound.columns),
        outbound.shape == inbound.shape,
        outbound.isnull().sum().equals(inbound.isnull().sum()),
        outbound.head(2).index.equals(inbound.head(2).index),
        outbound.tail(2).index.equals(inbound.tail(2).index)
    ]
    
    all_checks_pass = all(checks)
    if all_checks_pass:
        print(f"All checks pass for {key}: {all_checks_pass}")
        return True

fr_bidding_zone = 'FR'
fr_outbound = client.query_physical_crossborder_allborders(fr_bidding_zone, start, end, export=True, per_hour=True)
fr_inbound = client.query_physical_crossborder_allborders(fr_bidding_zone, start, end, export=False, per_hour=True)

no_bidding_zones = ['NO_1', 'NO_2', 'NO_3', 'NO_4', 'NO_5']
#not avail: 'NO_1A', 'NO_2A', 'NO_2_NSL'
no_outbound = {}
no_inbound = {}

for zone in no_bidding_zones:
    try:
        no_outbound[zone] = client.query_physical_crossborder_allborders(zone, start, end, export=True, per_hour=True)
    except KeyError:
        print(f"{zone} outbound not recognized, skipping")
        
    try:
        no_inbound[zone] = client.query_physical_crossborder_allborders(zone, start, end, export=False, per_hour=True)
    except KeyError:
        print(f"{zone} inbound not recognized, skipping")


if check_inbound_outbound_frames(fr_bidding_zone, fr_outbound, fr_inbound):
    fr_net = fr_outbound + fr_inbound

no_net = {}
for key in no_bidding_zones:
    if check_inbound_outbound_frames(key, no_outbound[key], no_inbound[key]):
        no_net[key] = no_outbound[key] + no_inbound[key]
        
        
   
  
    
    
