from entsoe import EntsoePandasClient
import pandas as pd

API_KEY = "***REMOVED***"

client = EntsoePandasClient(api_key=API_KEY)

start = pd.Timestamp('20171201', tz='Europe/Brussels')
end = pd.Timestamp('20180101', tz='Europe/Brussels')
country_code = 'FR'

all_borders = client.query_physical_crossborder_allborders(country_code, start, end, export=True, per_hour=True)
all_borders = client.query_physical_crossborder_allborders(country_code, start, end, export=False, per_hour=True)