import geopandas as gpd
import pandas as pd
import pandas_bokeh
import matplotlib.pyplot as plt
pandas_bokeh.output_notebook()
fp = r"E:\\immo_eliza_scrapping_group7\\BELGIUM_-_Municipalities.shp"
map_df = gpd.read_file(fp) 
map_df_copy = gpd.read_file(fp)
map_df.head()