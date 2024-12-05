import pandas as pd 
import numpy as np

df = pd.DataFrame([[["a", "b"]]], columns=("letters",))
st.dataframe(df)

df = pd.DataFrame([[np.array(["a", "b"])]], columns=("letters",))
st.dataframe(df)


df = pd.DataFrame([[tuple(["a", "b"])]], columns=("letters",))
st.dataframe(df)

df = pd.DataFrame([[set(["a", "b"])]], columns=("letters",))
st.dataframe(df)
