import streamlit as st  
import pandas as pd
import numpy as np

st.title("Estimation du montant de retrait")

# Parameters
with st.sidebar:
    st.logo("https://blog.iam-fp.com/images/logo_iam_horizontal_bleu.png",
    link="https://www.iam-fp.com/",
    icon_image="https://blog.iam-fp.com/images/logo_iam_horizontal_bleu.png")
    st.title("Paramètres")
    initial_amount = st.number_input("Montant de capital initial", min_value=0, max_value=pow(10,9), value=1250000)
    withdrawal_amount = st.number_input("Montant des retraits chaque année", min_value=0, max_value=pow(10,6), value=50000)
    exp_return = st.slider("Taux de revenus espéré (%)", value = 4.0, step = 0.1, min_value = 0.0, max_value = 12.0)
    horizon = st.slider("Horizon du placement (années)", value = 25, step = 1, min_value = 5, max_value = 30)
    marriage = st.toggle("Couple marié", value=False)

# Taux annuel mensualisé
monthly_rate = (1 + exp_return/100) ** (1/12) - 1

# Create fiscal data
data_fisca = pd.DataFrame({
    'Annee': range(1, horizon + 1),
    'PrlvtsSocx': [0.172] * horizon,
    'PFL': [0.075] * horizon,
    'PFO': [0.128] * horizon
})

# Generate base dataframe
data_gen = pd.DataFrame({
    'Mois': range(1, horizon * 12 + 1),
    'Capital': initial_amount,
    'PlusValue': 0.0,
    'PlusValueCumulee': 0.0,
    'Total': initial_amount,
    'Retrait': np.nan
})

# Main simulation loop
for i in range(1, horizon * 12):
    if (i + 1) % 12 == 0:  # End of year (adjusting for 0-based indexing)
        data_gen.loc[i, 'Capital'] = data_gen.loc[i-1, 'Capital']
        data_gen.loc[i, 'PlusValue'] = data_gen.loc[i-1, 'Total'] * monthly_rate
        data_gen.loc[i, 'PlusValueCumulee'] = data_gen.loc[i-1, 'PlusValueCumulee'] + data_gen.loc[i, 'PlusValue']
        
        # Withdrawal mechanics - proportional to Capital/PlusValue
        total_value = data_gen.loc[i, 'PlusValueCumulee'] + data_gen.loc[i, 'Capital']
        prop_pv = data_gen.loc[i, 'PlusValueCumulee'] / total_value
        prop_cap = data_gen.loc[i, 'Capital'] / total_value
        
        retrait_ar = withdrawal_amount * prop_cap
        retrait_pv = withdrawal_amount * prop_pv
        
        # Tax calculations
        year_index = int(i / 12)

        part_plvtSociaux = (retrait_pv /(1-data_fisca.loc[year_index, 'PrlvtsSocx']))- retrait_pv
        if ((i + 1) / 12) >= 8:
            if(marriage==False):
                retrait_pv2 = retrait_pv - 4600
            else:
                retrait_pv2 = retrait_pv - 9200
        else:
            retrait_pv2 = retrait_pv

        retrait_pv2 = max(0, retrait_pv2)
        part_pfo = (retrait_pv2 /(1-data_fisca.loc[year_index, 'PFO']))- retrait_pv2

        retrait_pv = retrait_pv + part_pfo + part_plvtSociaux
        retrait_apres_impots = retrait_pv + retrait_ar
        data_gen.loc[i, 'Retrait'] = retrait_apres_impots
        
        # Update amounts
        data_gen.loc[i, 'Capital'] -= prop_cap * retrait_apres_impots
        data_gen.loc[i, 'PlusValueCumulee'] -= prop_pv * retrait_apres_impots
        data_gen.loc[i, 'Total'] = data_gen.loc[i, 'Capital'] + data_gen.loc[i, 'PlusValueCumulee']
        
    else:
        data_gen.loc[i, 'Capital'] = data_gen.loc[i-1, 'Capital']
        data_gen.loc[i, 'PlusValue'] = data_gen.loc[i-1, 'Total'] * monthly_rate
        data_gen.loc[i, 'PlusValueCumulee'] = data_gen.loc[i-1, 'PlusValueCumulee'] + data_gen.loc[i, 'PlusValue']
        data_gen.loc[i, 'Total'] = data_gen.loc[i-1, 'Total'] + data_gen.loc[i, 'PlusValue']

st.header("Résultats de la simulation", divider="blue")
st.text(body = "Nous avons mis en place ce simulateur dans le but de vous montrer l'impact de la fiscalité sur des retraits récurrents en Assurance-Vie.",
        help = "Ce simulateur n'a pas de valeur contractuelle. Il n'engage pas la responsabilité de IAM Financial Partners et constitue simplement une illustration de l'impact de la fiscalité actuelle.")

# Représentation visuelles
st.subheader("Patrimoine Financier", divider="blue")
st.text("Votre patrimoine financier corresponsdant donc à la somme du capital et des plus-values.")
st.line_chart(data_gen['Total'], color = "#242943", y_label="Montant (€)", height=250)

st.subheader("Capital", divider="blue")
st.line_chart(data_gen['Capital'], color = "#242943", y_label="Montant (€)", height=250)

st.subheader("Plus value", divider="blue")
st.line_chart(data_gen['PlusValueCumulee'], color = "#242943", y_label="Montant (€)", x_label="Mois", height=250)

st.subheader("Retraits", divider="blue")
st.bar_chart(data_gen['Retrait'], color = "#242943", y_label="Montant (€)", x_label="Mois", height=250)

st.divider()

left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image(image = "https://blog.iam-fp.com/images/logo_iam_horizontal_bleu.png", width = 250)