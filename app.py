import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    'Dashboard de Vendas',
    layout='centered',
    initial_sidebar_state='expanded',
    menu_items={
        'Get Help':'https://github.com/hugomotadev',
        'About':'App desenvolvido no curso de Formação de Python - SENAC'
    }
)

df = pd.read_excel(r'.\assets\base_dados.xlsx')



#df
# criando sidebar
with st.sidebar:
    #st.subheader("Menu -dashboard de vendas")
    # criando lista suspensa
    fVendedor = st.selectbox(
        "Selecione o vendedor:",
        options=df['Vendedor'].unique()
    )
    
    fProduto = st.selectbox(
        "Selecione o Produto:",
        options=df['Produto vendido'].unique()
    )
    
    fCliente = st.selectbox(
        "Selecione o Cliente:",
        options=df['Cliente'].unique()
    )
    
    tabel_qtde_produto = df.loc[
        (df['Vendedor'] == fVendedor) &
        (df['Cliente'] == fCliente)]
    
#tabel_qtde_produto

# Tabela de quantidade de vendas por produto
tabel_qtde_produto = tabel_qtde_produto.drop(columns=['Data',
                                                      'Vendedor',
                                                      'Cliente',
                                                      'Nº pedido',
                                                      'Nº pedido',
                                                      'Região'])

tabel_qtde_produto = tabel_qtde_produto.groupby('Produto vendido').sum().reset_index()

#Tabela de Vendas e Margem
#st.subheader("Tabela - Venda margem")
tabel_vendas_margem = df.loc[
    (df['Vendedor'] == fVendedor) &
    (df['Produto vendido'] == fProduto) &
    (df['Cliente'] == fCliente)]

#tabel_vendas_margem

# Tabela de vendas por vendedor:
tabel_vendas_vendedor = df.loc[
    (df['Produto vendido'] == fProduto) &
    (df['Cliente'] == fCliente)]

#st.subheader("Nova tabela vendedor")
tabel_vendas_vendedor = tabel_vendas_vendedor.drop(columns = ['Data',
                                                              'Cliente',
                                                              'Região',
                                                              'Produto vendido',
                                                              'Nº pedido',
                                                              'Preço'])

tabel_vendas_vendedor = tabel_vendas_vendedor.groupby('Vendedor').sum().reset_index()

#tabel_vendas_vendedor

# Vendas por cliente

tabel_vendas_cliente = df.loc[(df['Vendedor'] == fVendedor) &
                              (df['Produto vendido'] == fProduto)]

tabel_vendas_cliente = tabel_vendas_cliente.drop(columns = ['Data',
                                                            'Região',
                                                            'Produto vendido',
                                                            'Nº pedido',
                                                            'Preço',
                                                            'Vendedor'])

tabel_vendas_cliente = tabel_vendas_cliente.groupby('Cliente').sum().reset_index()

#st.subheader("NOVA TABELA CLIENTE")
#tabel_vendas_cliente

# Gráfico de quantidade de produto em barra
graf1_qtde_produto = px.bar(tabel_qtde_produto,x='Produto vendido',
                            y='Quantidade',
                            title="Quantidade vendida por produto",
                            text_auto='.2s')

graf1_qtde_produto.update_traces(marker_color='green',
                                 marker_line_color='#fff',
                                 marker_line_width=1.5,
                                 opacity=0.6,
                                 textfont_size=12,
                                 textangle=0,
                                 textposition='outside',
                                 cliponaxis=False)

graf1_qtde_produto.update_layout(title_x=0.3)

#st.write(graf1_qtde_produto)

# Gráfico valor da venda por produto

graf2_valor_produto = px.bar(tabel_qtde_produto,x='Produto vendido',
                             y='Valor Pedido',
                             title='Valor total por produto')

#st.write(graf2_valor_produto)

# Gráfico total de venda por vendedor

graf3_total_vendedor = px.bar(tabel_vendas_vendedor,x='Vendedor',
                              y='Valor Pedido',
                              
                              title='Valor de venda por vendedor')
#graf3_total_vendedor



# Página inicial
st.header(":bar_chart: Dashboard de vendas")
st.write('---')
col1,col2,col3 = st.columns([2,2,3],gap='small')

total_vendas = round(tabel_vendas_margem['Valor Pedido'].sum(),2)
total_margem = round(tabel_vendas_margem['Margem Lucro'].sum(),2)
porc_margem = int(100*total_margem/total_vendas)

st.write('---')

with col1:
    st.metric("Vendas totais",value=f"R${total_vendas}")
    
with col2:
    st.metric("Margem total",value=f"R${total_margem}")

with col3:
    st.metric("Margem", value=f'{porc_margem}')
    
st.write(graf1_qtde_produto)
with st.expander("Visualização da tabela: "): #oculta e abrir
    st.write(tabel_qtde_produto)

st.write(graf2_valor_produto)
with st.expander('Visualização da tabela: '):
    st.write(tabel_qtde_produto)

st.write(graf3_total_vendedor)
with st.expander('Visualização da tabela: '):
    st.write(tabel_vendas_vendedor)
    

