import pandas as pd




# Planetbids
planetbids = 'planetbids_active_bids.csv'
df_planetbids = pd.read_csv(planetbids)
df_planetbids['bid_due_date'] = pd.to_datetime(df_planetbids['bid_due_date'], format='%m/%d/%Y')
df_filtered = df_planetbids[df_planetbids['bid_due_date'] > '2025-03-23']

# Sort by states
df_san_diego = df_filtered[df_filtered['county'] == 'San Diego'] # San Diego
df_imperial = df_filtered[df_filtered['county'] == 'Imperial'] # Imperial
df_orange = df_filtered[df_filtered['county'] == 'Orange'] # Orange
df_riverside = df_filtered[df_filtered['county'] == 'Riverside'] # Riverside
df_san_bernardino = df_filtered[df_filtered['county'] == 'San Bernardino'] # San Bernardino
df_los_angeles = df_filtered[df_filtered['county'] == 'Los Angeles'] # Los Angeles
df_ventura = df_filtered[df_filtered['county'] == 'Ventura'] # Ventura
df_santa_barbara = df_filtered[df_filtered['county'] == 'Santa Barbara'] # Santa Barbara

# Save each DataFrame to a separate CSV file
df_san_diego.to_csv('san_diego.csv', index=False)
df_imperial.to_csv('imperial.csv', index=False)
df_orange.to_csv('orange.csv', index=False)
df_riverside.to_csv('riverside.csv', index=False)
df_san_bernardino.to_csv('san_bernardino.csv', index=False)
df_los_angeles.to_csv('los_angeles.csv', index=False)
df_ventura.to_csv('ventura.csv', index=False)
df_santa_barbara.to_csv('santa_barbara.csv', index=False)










# SAM.gov
sam_gov = 'finalized_sam_gov.csv'
df_sam = pd.read_csv(sam_gov)