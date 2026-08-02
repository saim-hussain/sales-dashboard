import pandas as pd
import os
def load_superstore_data():
    """Load and clean the Superstore dataset."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, 'data', 'Sample - Superstore.csv')
    
    df = pd.read_csv(csv_path, encoding='latin-1')

    # cleaning column names
    df.columns = [col.strip().lower().replace(' ','_') for col in df.columns]

    # converting dates
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['ship_date'] = pd.to_datetime(df['ship_date'])

    #ensuring discount remains between 0 and 1
    df['discount'] = df['discount'].clip(0,1)

    #ensuring that sales remain positive
    df['sales'] = df['sales'].abs()

    return df

if __name__ == "__main__":
    df = load_superstore_data()
    print("Shape:", df.shape)
    print("Column:", list(df.columns))
    print(df.head(3))