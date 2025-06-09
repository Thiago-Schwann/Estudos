import pandas as pd
import matplotlib.pyplot as plt


ano = 2024
caminho_dados = f'{ano}_Viagem.csv' #Arquivo CSV impossibilita o push
caminho_saida_tabela = f'tabela_{ano}.xlsx'
caminho_saida_grafico = f'grafico_{ano}.png'

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:.2f}'.format)

df_viagens = pd.read_csv(caminho_dados, encoding='Windows-1252', sep=';', decimal=",")

df_viagens['Despesas'] = df_viagens['Valor diárias'] + df_viagens['Valor passagens'] + df_viagens['Valor outros gastos']

df_viagens['Cargo'] = df_viagens['Cargo'].fillna("NÃO IDENTIFICADO")

df_viagens["Período - Data de início"] = pd.to_datetime(df_viagens["Período - Data de início"], format="%d/%m/%Y")
df_viagens["Período - Data de fim"] = pd.to_datetime(df_viagens["Período - Data de fim"], format="%d/%m/%Y")

df_viagens['Mês da viagem'] = df_viagens['Período - Data de início'].dt.month_name()
df_viagens['Dias de viagem'] = (df_viagens['Período - Data de fim'] - df_viagens['Período - Data de início']).dt.days

df_viagens_consolidado = (df_viagens
 .groupby('Cargo')
 .agg(
    despesa_media=('Despesas', 'mean'),
    duracao_media=('Dias de viagem', 'mean'),
    despesas_totais=('Despesas', 'sum'),
    destino_mais_frequente=('Destinos', pd.Series.mode),
    n_viagens=('Nome', 'count')
    )
 .reset_index()
 .sort_values(by='despesas_totais', ascending=False))

df_cargos = df_viagens['Cargo'].value_counts(normalize=True).reset_index()
cargos_relevantes = df_cargos.loc[df_cargos['proportion'] > 0.01, 'Cargo']
filtro = df_viagens_consolidado['Cargo'].isin(cargos_relevantes)

df_final = df_viagens_consolidado[filtro].sort_values(by='n_viagens', ascending=False)

df_final.to_excel(caminho_saida_tabela, index=False)

fig, ax = plt.subplots(figsize=(16, 6))

ax.barh(df_final['Cargo'], df_final['despesa_media'], color="#49deac")
ax.invert_yaxis()

ax.set_facecolor('#3b3b47')
fig.suptitle('Despesa média em viagens por cargo público (2023)')
plt.figtext(0.65, 0.89, 'Fonte: Portal da Transparência', fontsize=8)
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.yticks(fontsize=8)
plt.xlabel('Despesa média')

plt.savefig(caminho_saida_grafico, bbox_inches='tight')