import random
from datetime import datetime, timedelta
import pandas as pd

# Define the list of component descriptions
comp_desc_options = ['engine']

# Function to generate fake oil analysis data
def generate_fake_oil_data(num_samples):
    fake_data = []
    for _ in range(num_samples):
        equip_number = f"{random.randint(1, 5):02d}"
        comp_desc = random.choice(comp_desc_options)
        sample_dt = datetime.now() - timedelta(days=random.randint(0, int((datetime.now() - datetime(2020, 1, 1)).days)))
        
        # Generate random values for the elements
        al = random.uniform(0, 200)
        cr = random.uniform(0, 200)
        cu = random.uniform(0, 200)
        fe = random.uniform(0, 200)
        k = random.uniform(0, 200)
        na = random.uniform(0, 200)
        ni = random.uniform(0, 200)
        pb = random.uniform(0, 200)
        si = random.uniform(0, 200)
        sn = random.uniform(0, 200)
        ag = random.uniform(0, 200)
        
        fake_data.append({
            'equip_number': equip_number,
            'comp_desc': comp_desc,
            'sample_dt': sample_dt.strftime('%Y-%m-%d'),
            'al': al,
            'cr': cr,
            'cu': cu,
            'fe': fe,
            'k': k,
            'na': na,
            'ni': ni,
            'pb': pb,
            'si': si,
            'sn': sn,
            'ag': ag
        })
    return fake_data

# Function to save the data as a CSV file with specified parameters
def save_fake_oil_data(num_samples, mine, fleet, prefix):
    fake_data = generate_fake_oil_data(num_samples)

    # Add MINE and FLEET columns
    for record in fake_data:
        record['mine'] = mine
        record['fleet'] = fleet

    # Create a DataFrame from the data
    df = pd.DataFrame(fake_data)

    # Add prefix to equip_number
    df['equip_number'] = prefix + df['equip_number']

    # Reorder columns to have MINE and FLEET as the first two columns
    df = df[['mine', 'fleet'] + [col for col in df.columns if col not in ['mine', 'fleet']]]

    # Save the DataFrame as a CSV file
    df.to_csv(f'{mine}_{fleet}.csv', index=False)

# Example usage: Generate 10 fake oil analysis records and save them with specified parameters
save_fake_oil_data(100, 'S11D', '785C', 'CA')
save_fake_oil_data(100, 'S11D', '793F', 'CM')
