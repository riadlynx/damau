import matplotlib.pyplot as pit
import pandas as pd

df = pd.read_excel('test.xlsx','Sheet1',)
pit.plot(df['time'],df['WL'])

pit.xlabel('time per year')
pit.ylabel('hauteur')
pit.title('hauteur dans le temps')
pit.legend()

pit.show()
