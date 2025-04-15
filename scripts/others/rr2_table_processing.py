import pandas as pd

rr2_rating_tables = pd.ExcelFile('rr2_tables/fema_appendix-d-rating-factor-tables_02242023.xlsx')
rr2_rating_tables.sheet_names
# for sheet in rr2_rating_tables.sheet_names:
#     df = pd.read_excel(rr2_rating_tables,sheet_name=sheet)
#     df.to_excel("rr2_tables/"+f"{sheet}.xlsx",index=False)
    
# Base rates NL
df = pd.read_excel(rr2_rating_tables,sheet_name='BaseRates - NL', skiprows = 14)   # rr2_rating_tables.sheet_names[2] 
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Region','Segment','Single & 2-4 Family Home Indicator','  Inland Flood Building','  Inland Flood Contents',' Storm Surge Non-Barrier Island Building',' Storm Surge Non-Barrier Island Contents',' Storm Surge Barrier Island Building',' Storm Surge Barrier Island Contents','  Tsunami Building','  Tsunami Contents','  Great Lakes Building','  Great Lakes Contents','  Coastal Erosion Building','  Coastal Erosion Contents']
df.to_csv('rr2_tables/BaseRates - NL.csv',index=False)

# Base rates L
df = pd.read_excel(rr2_rating_tables,sheet_name='BaseRates - L', skiprows = 14)  
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Region','Segment','Single & 2-4 Family Home Indicator','Inland Flood Fluvial Building','Inland Flood Fluvial Contents','Inland Flood Pluvial Building','Inland Flood Pluvial Contents','Storm Surge Building','Storm Surge Contents','Tsunami Building','Tsunami Contents','Great Lakes Building','Great Lakes Contents','Coastal Erosion Building','Coastal Erosion Contents',]
df.to_csv('rr2_tables/BaseRates - L.csv',index=False)
    
#DTR NL
df = pd.read_excel(rr2_rating_tables,sheet_name='DTR - NL', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Region','Distance to River (meters)','Inland Flood',]
df = df.dropna()
df.to_csv('rr2_tables/DTR - NL.csv',index=False)

#DTR L
df = pd.read_excel(rr2_rating_tables,sheet_name='DTR - L', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Distance to River (meters)','Fluvial','Pluvial']
df = df.dropna()
df.to_csv('rr2_tables/DTR - L.csv',index=False)

#DTR NL
df = pd.read_excel(rr2_rating_tables,sheet_name='DTR - NL', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Region','Distance to River (meters)','Inland Flood',]
df = df.dropna()
df.to_csv('rr2_tables/DTR - NL.csv',index=False)

#ElevRelRiver NL
df = pd.read_excel(rr2_rating_tables,sheet_name='ElevRelRiver - NL - Seg 1-4', skiprows = 14)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['River Class','Elevation Relative to River (feet)','Inland Flood Segment 1','Inland Flood Segment 2','Inland Flood Segment 3','Inland Flood Segment 4',]
df = df.dropna()
df.to_csv('rr2_tables/ElevRelRiver - NL - Seg 1-4.csv',index=False)

#ElevRelRiver L
df = pd.read_excel(rr2_rating_tables,sheet_name='ElevRelRiver - L', skiprows = 14)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['River Class','Elevation Relative to River (feet)','Inland Flood Fluvial','Inland Flood Pluvial',]
df = df.dropna()
df.to_csv('rr2_tables/ElevRelRiver - L.csv',index=False)

#DrainageArea NL
df = pd.read_excel(rr2_rating_tables,sheet_name='DrainageArea - NL - Seg 1-4', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Drainage Area (km2)','Inland Flood Segment 1','Inland Flood Segment 2','Inland Flood Segment 3','Inland Flood Segment 4',]
df = df.dropna()
df.to_csv('rr2_tables/DrainageArea - NL.csv',index=False)

#DrainageArea L
df = pd.read_excel(rr2_rating_tables,sheet_name='DrainageArea - L', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Drainage Area (km2)','Inland Flood Fluvial','Inland Flood Pluvial',]
df = df.dropna()
df.to_csv('rr2_tables/DrainageArea - L.csv',index=False)

#StructRelElev NL
df = pd.read_excel(rr2_rating_tables,sheet_name='StructRelElev - NL', skiprows = 14)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Region','Structural Relative Elevation (feet)','Inland Flood',]
df = df.dropna()
df.to_csv('rr2_tables/StructRelElev - NL.csv',index=False)

#StructRelElev L
df = pd.read_excel(rr2_rating_tables,sheet_name='StructRelElev - L', skiprows = 14)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Structural Relative Elevation (feet)','Inland Flood Fluvial','Inland Flood Pluvial',]
df = df.dropna()
df.to_csv('rr2_tables/StructRelElev - L.csv',index=False)

#DTC NL
df = pd.read_excel(rr2_rating_tables,sheet_name='DTC - Non-BI - NL', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Region','Distance to Coast (meters)','Storm Surge','Tsunami']
df = df.dropna()
df.to_csv('rr2_tables/DTC - Non-BI - NL.csv',index=False)

#DTC L
df = pd.read_excel(rr2_rating_tables,sheet_name='DTC - SS - L', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Region','Distance to Coast (meters)','Storm Surge',]
df = df.dropna()
df.to_csv('rr2_tables/DTC - SS - L.csv',index=False)

#CE NL
df = pd.read_excel(rr2_rating_tables,sheet_name='DTC - CE - NL', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Distance to Coast (meters)','Coastal Erosion']
df = df.dropna()
df.to_csv('rr2_tables/DTC - CE - NL.csv',index=False)

#CE L
df = pd.read_excel(rr2_rating_tables,sheet_name='DTC - CE - L', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Distance to Coast (meters)','Coastal Erosion']
df = df.dropna()
df.to_csv('rr2_tables/DTC - CE - L.csv',index=False)

#Elevation NL
df = pd.read_excel(rr2_rating_tables,sheet_name='Elevation - Non-BI - NL', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Region','Elevation (feet)','Storm Surge','Tsunami']
df = df.dropna()
df.to_csv('rr2_tables/Elevation - Non-BI - NL.csv',index=False)

#Elevation L
df = pd.read_excel(rr2_rating_tables,sheet_name='Elevation - IFSS - L', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Region','Elevation (feet)','Inland Flood Fluvial','Inland Flood Pluvial','Storm Surge',]
df = df.dropna()
df.to_csv('rr2_tables/Elevation - IFSS - L.csv',index=False)

#Territory NL
df = pd.read_excel(rr2_rating_tables,sheet_name='Territory - Non-BI - NL', skiprows = 12)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
#df.columns = ['Region','Elevation (feet)','Storm Surge','Tsunami']
df.to_csv('rr2_tables/Territory - Non-BI - NL.csv',index=False)

#Territory L
df = pd.read_excel(rr2_rating_tables,sheet_name='Territory - IFSS - L', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
columns = df.columns.tolist()
columns[1] = "Levee System ID"
df.columns = columns
df.to_csv('rr2_tables/Territory - IFSS - L.csv',index=False)

#Levee Quality L IF
df = pd.read_excel(rr2_rating_tables,sheet_name='Levee Quality-IF', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Levee System ID','Annual Probability of Failing Prior to Overtopping','Overtopping Return Period','Levee Quality Factor']
df.to_csv('rr2_tables/Levee Quality-IF.csv',index=False)

#Levee Quality L SS
df = pd.read_excel(rr2_rating_tables,sheet_name='Levee Quality-SS', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Levee System ID','Annual Probability of Failing Prior to Overtopping','Overtopping Return Period']
df.to_csv('rr2_tables/Levee Quality-SS.csv',index=False)

#Type of Use
df = pd.read_excel(rr2_rating_tables,sheet_name='Type of Use', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Type of Use','Inland Flood','Storm Surge','Tsunami', 'Great Lakes']
df.to_csv('rr2_tables/Type of Use.csv',index=False)

#Floors of Interest
df = pd.read_excel(rr2_rating_tables,sheet_name='Floors of Interest', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns[:4]]
df = df[1:]
df.iloc[2,2] = 3
df.columns = ['Single & 2-4 Family Home Indicator','Condo Unit Owner Indicator','Floors of Interest','All Perils, Excluding Coastal Erosion',]
df.to_csv('rr2_tables/Floors of Interest.csv',index=False)

#Foundation Type
df = pd.read_excel(rr2_rating_tables,sheet_name='Foundation Type', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns[:2]]
df = df[1:]
df.columns = ['Foundation Type','All Perils, Excluding Coastal Erosion',]
df.to_csv('rr2_tables/Foundation Type.csv',index=False)

#First Floor Height
df = pd.read_excel(rr2_rating_tables,sheet_name='First Floor Height', skiprows = 14)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['First Floor Height (feet)','Open, No Obstruction With Flood Vents','Open, No Obstruction No Flood Vents','Open, Obstruction With Flood Vents','Open, Obstruction No Flood Vents','Closed, Wall With Flood Vents','Closed, Wall No Flood Vents',]
df = df.dropna()
df.to_csv('rr2_tables/First Floor Height.csv',index=False)

#Building Value
df = pd.read_excel(rr2_rating_tables,sheet_name='Building Value', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Building Value','All Perils, Excluding Coastal Erosion',]
df = df.dropna()
df.to_csv('rr2_tables/Building Value.csv',index=False)

#Contents Value
df = pd.read_excel(rr2_rating_tables,sheet_name='Contents Value', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Contents Value','All Perils, Excluding Coastal Erosion',]
df = df.dropna()
df.to_csv('rr2_tables/Contents Value.csv',index=False)

#RCV Caps
df = pd.read_excel(rr2_rating_tables,sheet_name='RCV Caps', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
#df.columns = ['Contents Value','All Perils, Excluding Coastal Erosion',]
df.to_csv('rr2_tables/RCV Caps.csv',index=False)


#Deductible Limit ITV Cov A
df = pd.read_excel(rr2_rating_tables,sheet_name='Deductible Limit ITV Cov A', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Deductible & Limit to Coverage Value Ratio','Inland Flood','Storm Surge, Tsunami, Great Lakes, and Coastal Erosion']
df = df.dropna()
df.to_csv('rr2_tables/Deductible Limit ITV Cov A.csv',index=False)

#Deductible Limit ITV Cov C
df = pd.read_excel(rr2_rating_tables,sheet_name='Deductible Limit ITV Cov C', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Deductible & Limit to Coverage Value Ratio','Inland Flood','Storm Surge, Tsunami, Great Lakes, and Coastal Erosion']
df = df.dropna()
df.to_csv('rr2_tables/Deductible Limit ITV Cov C.csv',index=False)

#Deductible ITV Cov A
df = pd.read_excel(rr2_rating_tables,sheet_name='Deductible ITV Cov A', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Deductible to Coverage Value Ratio','Inland Flood','Storm Surge, Tsunami, Great Lakes, and Coastal Erosion']
df = df.dropna()
df.to_csv('rr2_tables/Deductible ITV Cov A.csv',index=False)

#Deductible ITV Cov C
df = pd.read_excel(rr2_rating_tables,sheet_name='Deductible ITV Cov C', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Deductible to Coverage Value Ratio','Inland Flood','Storm Surge, Tsunami, Great Lakes, and Coastal Erosion']
df = df.dropna()
df.to_csv('rr2_tables/Deductible ITV Cov C.csv',index=False)


# Concentration Risk
df = pd.read_excel(rr2_rating_tables,sheet_name='Concentration Risk', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['Concentration Risk Code','Concentration Risk Territory Description (Note 1)','Inland Flood','Storm Surge']
df.to_csv('rr2_tables/Concentration Risk.csv',index=False)


# Concentration Risk Mapping
df = pd.read_excel(rr2_rating_tables,sheet_name='Concentration Risk Mapping', skiprows = 13)  
df.columns
columns = [i for i in df.columns if "Unnamed" not in i]

df = df[columns]
df = df[1:]
df.columns = ['State','County','Concentration Risk Territory']
df.to_csv('rr2_tables/Concentration Risk Mapping.csv',index=False)

  
    