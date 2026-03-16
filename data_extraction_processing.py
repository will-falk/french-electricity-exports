from entsoe import EntsoePandasClient
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN_ENTSOE = os.getenv("API_TOKEN_ENTSOE")
client = EntsoePandasClient(api_key=API_TOKEN_ENTSOE)

start = pd.Timestamp('20250101', tz='Europe/Brussels')
end = pd.Timestamp.now(tz='Europe/Brussels') - pd.Timedelta(days=1)

#checks that both dfs have compatible shapes
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

# get fr inbound and outbound (single bidding zone)
fr_bidding_zone = 'FR'
fr_outbound = client.query_physical_crossborder_allborders(fr_bidding_zone, start, end, export=True, per_hour=True)
fr_inbound = client.query_physical_crossborder_allborders(fr_bidding_zone, start, end, export=False, per_hour=True)

#get no inbound and outbound (multiple bidding zones), inactive = ['NO_1A', 'NO_2A', 'NO_2_NSL']
no_bidding_zones_active = ['NO_1', 'NO_2', 'NO_3', 'NO_4', 'NO_5']
no_outbound = {}
no_inbound = {}

for zone in no_bidding_zones_active:
    try:
        no_outbound[zone] = client.query_physical_crossborder_allborders(zone, start, end, export=True, per_hour=True)
    except KeyError:
        print(f"{zone} outbound not recognized, skipping")
        
    try:
        no_inbound[zone] = client.query_physical_crossborder_allborders(zone, start, end, export=False, per_hour=True)
    except KeyError:
        print(f"{zone} inbound not recognized, skipping")


# check and net fr inbound and outbound
if check_inbound_outbound_frames(fr_bidding_zone, fr_outbound, fr_inbound):
    fr_net = fr_inbound - fr_outbound

#check and net no inbound and outbound
no_net = {}
for key in no_bidding_zones_active:
    if check_inbound_outbound_frames(key, no_outbound[key], no_inbound[key]):
        no_net[key] = no_inbound[key] - no_outbound[key]


#drop no domestic bidding zones
no_net_cleaned = []
for df in no_net.values():
    cols_to_drop = [col for col in df.columns if col in no_bidding_zones_active]
    df_cleaned = df.drop(columns=cols_to_drop)
    no_net_cleaned.append(df_cleaned)

#condense all no foreign bidding zones into a single df
no_net_cleaned_condensed = no_net_cleaned[0]
for df in no_net_cleaned[1:]:
    no_net_cleaned_condensed = no_net_cleaned_condensed.add(df, fill_value=0)


#define periodizations
time_periods = {
    "daily": "D",
    "weekly": "W",
    "monthly": "ME"
}

#periodize fr net
fr_final_frames_by_period = {}
for key, rule in time_periods.items():
    fr_final_frames_by_period[key] = fr_net.resample(rule).sum()

#periodize no net
no_final_frames_by_period = {}
for key, rule in time_periods.items():
    no_final_frames_by_period[key] = no_net_cleaned_condensed.resample(rule).sum()


# no exports for validation
# for zone, df in no_net.items():
#     df.to_csv(f"no_net_{zone}.csv", index=True)

# no_net_cleaned_condensed.to_csv("no_net_cleaned_condensed.csv", index=True)

# for period, df in no_final_frames_by_period.items():
#     df.to_csv(f"no_final_{period}.csv", index=True)



#france exports for validation   
# fr_outbound.to_csv(f"fr_out.csv", index=True)
# fr_inbound.to_csv(f"fr_in.csv", index=True)

# fr_net.to_csv("fr_net.csv", index=True)

# for period, df in fr_net_frames_by_period.items():
#     df.to_csv(f"fr_net_{period}.csv", index=True)