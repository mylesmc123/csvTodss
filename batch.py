# %%
from pydsstools.heclib.dss import HecDss
from datetime import datetime
from pydsstools.core import TimeSeriesContainer, UNDEFINED
import pandas as pd
import os
# %%
dss_output_file = 'GLO_nonTC_Mar2022_BC_NAVD88.dss'
input_dir = r'V:\projects\p00659_dec_glo_phase3\02_analysis\nonTropical Calibration Event Selection\tidal_gage_data'
# find all the csv files in the input_dir
input_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.csv')]
input_files
# %%
# setup dictionarry to assigned a BC Line name to the corresponding csv file
bc_line_dict = {
    'Gulf': 'V:\\projects\\p00659_dec_glo_phase3\\02_analysis\\nonTropical Calibration Event Selection\\tidal_gage_data\\NOAA_8771341_Galveston Bay Entrance_NonTC_Mar2022.csv',
    'East_Bay': 'V:\\projects\\p00659_dec_glo_phase3\\02_analysis\\nonTropical Calibration Event Selection\\tidal_gage_data\\NOAA_8771013_Eagle Point_nonTC_Mar2022.csv',
    'Galveston_Inlet': 'V:\\projects\\p00659_dec_glo_phase3\\02_analysis\\nonTropical Calibration Event Selection\\tidal_gage_data\\NOAA_8771013_Eagle Point_nonTC_Mar2022.csv',
    'Trinity_Bay': 'V:\\projects\\p00659_dec_glo_phase3\\02_analysis\\nonTropical Calibration Event Selection\\tidal_gage_data\\NOAA_8771013_Eagle Point_nonTC_Mar2022.csv',
    'ICWW': 'V:\\projects\\p00659_dec_glo_phase3\\02_analysis\\nonTropical Calibration Event Selection\\tidal_gage_data\\NOAA_8770808_High Island_nonTC_Mar2022.csv',
}
bc_line_dict
# %%
# create a dataframe to store the data
df = pd.DataFrame()
# loop through the dictionary and read the csv file
for bc_line, file in bc_line_dict.items():
    print(str(file))
    df = pd.read_csv(file, skiprows=3, header=None, names=['Date', 'Time', 'Stage'], parse_dates=[['Date', 'Time']], index_col='Date_Time')
    gage_name = os.path.basename(file).split('_')[1]  
    print(gage_name)
    pathname = f'/{bc_line}/{gage_name}/STAGE//IR-MONTH/NOAA NAVD88/'
    tsc = TimeSeriesContainer()
    tsc.pathname = pathname
    tsc.startDateTime = df.index[0].strftime("%d%b%Y %H:%M:%S")
    tsc.numberValues = len(df["Stage"])
    tsc.units = "FEET"
    tsc.type = "INST"
    tsc.interval = -1
    tsc.values = df["Stage"].tolist()
    tsc.times = df.index.strftime("%d%b%Y %H:%M:%S").astype(str).tolist()
    
    with HecDss.Open(dss_output_file) as fid:
            status = fid.put_ts(tsc)
# %%