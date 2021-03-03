import pandas as pd 
from pathlib import Path

class_register_dir = Path.cwd() / 'class-registers'
class_register = pd.read_excel(class_register_dir / 'EEE2045F_all.xlsx')
print(class_register.