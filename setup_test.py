import pandas as pd

csv_input = pd.read_csv('copy_big.csv')

#csv_input["RF_x"] = 200
#csv_input["RF_y"] = 200

#csv_input.to_csv('copy_big.csv', index=False)


print(csv_input.max(axis=1))