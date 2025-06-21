from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
df = pd.read_csv(app_dir / "donnees-de-vaccination-par-commune.csv")
