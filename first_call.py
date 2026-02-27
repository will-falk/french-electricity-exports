from entsoe import EntsoePandasClient
import pandas as pd

API_KEY = "***REMOVED***"

client = EntsoePandasClient(api_key=API_KEY)

start = pd.Timestamp('20250101', tz='Europe/Brussels')
end = pd.Timestamp.now(tz='Europe/Brussels') - pd.Timedelta(days=1)
# end = pd.Timestamp('20251231', tz='Europe/Brussels')

fr_country_code = 'FR'
no_country_code = 'NO'

fr_all_borders_outbound = client.query_physical_crossborder_allborders(country_code, start, end, export=True, per_hour=True)
fr_all_borders_inbound = client.query_physical_crossborder_allborders(country_code, start, end, export=False, per_hour=True)

no_all_borders_outbound = client.query_physical_crossborder_allborders(country_code, start, end, export=True, per_hour=True)
no_all_borders_inbound = client.query_physical_crossborder_allborders(country_code, start, end, export=False, per_hour=True)