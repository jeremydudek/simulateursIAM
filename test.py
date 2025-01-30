# Plotting Total
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(data_gen['Mois'], data_gen['Total'], label='Total')
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
plt.xlabel('Mois')
plt.ylabel('Montant')
plt.title('Patrimoine financier')
plt.grid(False)
st.pyplot(fig)

# Plotting Total
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(data_gen['Mois'], data_gen['Capital'], label='Capital')
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
plt.xlabel('Mois')
plt.ylabel('Montant')
plt.title('Capital')
plt.grid(False)
st.pyplot(fig)

# Plotting Total
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(data_gen['Mois'], data_gen['PlusValueCumulee'], label='Plus Value Cumulée')
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
plt.xlabel('Mois')
plt.ylabel('Montant')
plt.title('Plus Value réalisée')
plt.grid(False)
st.pyplot(fig)

# Plotting Total
fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(data_gen['Mois'], data_gen['Retrait'], label='Retrait')
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
plt.xlabel('Mois')
plt.ylabel('Montant')
plt.title('Montant des retraits avant impôts')
plt.grid(False)
st.pyplot(fig)