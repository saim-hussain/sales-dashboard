import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.load import load_all

if __name__ == "__main__":
    print("🌱 Seeding database...")
    load_all()
    print("🎉 Done!")