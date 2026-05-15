import pandas as pd
import numpy as np
import os
import uuid
from datetime import datetime, timedelta

def generate_synthetic_cnes_data(num_records=50):

    # synthetic data simulating the CNES database
    np.random.seed(42)
    
    facility_types = ['HEALTH POST', 'HEALTH CENTER/BASIC UNIT', 'GENERAL HOSPITAL', 'CLINIC/SPECIALTY CENTER']
    municipalities = ['SAO PAULO', 'GUARULHOS', 'CAMPINAS', 'SÃO BERNARDO DO CAMPO', 'SANTO ANDRÉ']
    
    data = {
        'cnes': [str(np.random.randint(1000000, 9999999)) for _ in range(num_records)],
        'facility_name': [f'HEALTH FACILITY {i}' for i in range(num_records)],
        'facility_type': np.random.choice(facility_types, num_record),
        'municipality': np.random.choice(municipalities, num_records),
        'state': ['SP'] * num_records,
        'latitude': np.random.uniform(-23.8, -22.8, num_records),
        'longitude': np.random.uniform(-47.0, -46.0, num_records)
    }

    return pd.DataFrame(data)

def generate_synthetic_sisreg_data(df_cnes, num_records=5000):

    # synthetic data simulating the SISREG database
    np.random.seed(42)
    
    cnes_list = df_cnes['cnes'].tolist()
    status_list = ['ATTENDED', 'NO_SHOW', 'CANCELLED', 'PENDING']
    procedures = ['CARDIOLOGY CONSULTATION', 'OPHTHALMOLOGY CONSULTATION', 'ULTRASOUND', 'TOMOGRAPHY', 'ORTHOPEDIC CONSULTATION']
    
    request_dates = [datetime(2025, 1, 1) + timedelta(days=np.random.randint(0, 365)) for _ in range(num_records)]
    wait_times = np.random.exponential(scale=45, size=num_records).astype(int)
    
    appointment_dates = [d + timedelta(days=int(t)) for d, t in zip(request_dates, wait_times)]
    
    # correlation: longer wait time -> higher chance of no-show
    prob_no_show = 0.1 + (wait_times / 365) * 0.5
    prob_no_show = np.clip(prob_no_show, 0, 0.8)
    
    final_status = []

    for p in prob_no_show:
        if np.random.random() < p:
            final_status.append('NO_SHOW')

        else:
            final_status.append(np.random.choice(['ATTENDED', 'ATTENDED', 'ATTENDED', 'CANCELLED']))
            
    # dirty data (NaNs, inconsistencies)
    dirty_status = final_status.copy()

    for i in range(int(num_records * 0.05)):
        dirty_status[np.random.randint(0, num_records)] = np.nan
        dirty_status[np.random.randint(0, num_records)] = 'NO_SHW'
        
    data = {
        'appointment_id': [str(uuid.uuid4()) for _ in range(num_records)],
        'patient_id': [str(uuid.uuid4()) for _ in range(num_records)],
        'requesting_cnes': np.random.choice(cnes_list, num_records),
        'executing_cnes': np.random.choice(cnes_list, num_records),
        'request_date': request_dates,
        'appointment_date': appointment_dates,
        'procedure': np.random.choice(procedures, num_records),
        'status': dirty_status,
        'distance_km': np.random.exponential(scale=15, size=num_records)
    }
    
    # inserting some NaNs in distance
    df = pd.DataFrame(data)
    df.loc[np.random.choice(df.index, size=int(num_records * 0.02)), 'distance_km'] = np.nan
    
    return df

def execute_etl():
    
    print("Starting SUSi ETL Pipeline...")
    
    # EXTRACTION
    print("1. Extracting data...")
    df_cnes_raw = generate_synthetic_cnes_data()
    df_sisreg_raw = generate_synthetic_sisreg_data(df_cnes_raw)
    
    print(f"- CNES records extracted: {len(df_cnes_raw)}")
    print(f"- SISREG records extracted: {len(df_sisreg_raw)}")
    
    # TRANSFORMATION
    print("\n2. Transforming and cleaning data...")
    df_sisreg = df_sisreg_raw.copy()
    
    # NaNs
    nulls_before = df_sisreg['status'].isna().sum()
    df_sisreg['status'] = df_sisreg['status'].fillna('UNKNOWN')
    print(f"- {nulls_before} null values in 'status' column filled with 'UNKNOWN'.")
    
    nulls_dist = df_sisreg['distance_km'].isna().sum()
    median_dist = df_sisreg['distance_km'].median()
    df_sisreg['distance_km'] = df_sisreg['distance_km'].fillna(median_dist)
    print(f"- {nulls_dist} null values in 'distance_km' column imputed with median ({median_dist:.2f} km).")
    
    # grouping errors
    errors_before = (df_sisreg['status'] == 'NO_SHW').sum()
    df_sisreg['status'] = df_sisreg['status'].replace({'NO_SHW': 'NO_SHOW'})
    print(f"- {errors_before} typos ('NO_SHW') corrected to 'NO_SHOW'.")
    
    df_sisreg['wait_time_days'] = (df_sisreg['appointment_date'] - df_sisreg['request_date']).dt.days
    df_sisreg['negative_outcome'] = df_sisreg['status'].isin(['NO_SHOW', 'CANCELLED']).astype(int)
    print("- New features 'wait_time_days' and 'negative_outcome' created.")
    
    df_final = pd.merge(
        df_sisreg, 
        df_cnes_raw[['cnes', 'municipality', 'facility_type']], 
        left_on='executing_cnes', 
        right_on='cnes', 
        how='left'
    )
    df_final = df_final.drop('cnes', axis=1)

    print("- SISREG and CNES databases merged successfully.")
    
    # LOAD
    print("\n3. Loading processed data...")
    os.makedirs('/home/gathddu/Documents/SUSi/data/processed', exist_ok=True)
    output_path = '/home/gathddu/Documents/SUSi/data/processed/base.csv'
    df_final.to_csv(output_path, index=False)
    print(f"- Final database exported to: {output_path}")
    print(f"- Total records processed: {len(df_final)}")
    print("ETL Pipeline completed successfully.")

if __name__ == "__main__":
    execute_etl()