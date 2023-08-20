import yfinance as yf
import altair as alt
import pandas as pd
import streamlit as st

# Lista de tickers predefinidos
tickers = ["^NDX", "CL=F", "GC=F", "SI=F", "EURUSD=X", "BTC-USD", "ETH-USD"]


st.title("Evolución de Bonos y Commodities")

selected_tickers = st.multiselect("Selecciona acciones", tickers, default=tickers[:1])
start_date = st.date_input('Fecha Inicial', value = pd.to_datetime("2017-01-31"))
end_date = st.date_input("Fecha Final", value = pd.to_datetime("today"))


st.markdown("""---""")


# Función para obtener los datos de Yahoo Finance
@st.cache_data
def get_data(selected_tickers):
    if not selected_tickers:
        return pd.DataFrame()
    data_list = [yf.download(ticker, start=start_date, end= end_date) for ticker in selected_tickers]
    combined_data = pd.concat(data_list, keys=selected_tickers, names=["symbol"])
    combined_data.reset_index(inplace=True)
    return combined_data

# Sidebar con la selección de acciones

source = get_data(selected_tickers)
source["Retorno Acumulado"] = source.groupby("symbol")["Close"].pct_change().add(1).cumprod() - 1
source = source.fillna(0)


data_bonds = pd.read_csv("Resumen Bonos Bolivia 4.5 20-MAR-2028.csv", index_col=0, encoding='utf-8', sep= ',' )
data_bonds.index = pd.to_datetime(data_bonds.index, format='%d.%m.%Y')

# Formatear las fechas nuevamente al formato "YYYY-MM-DD"
data_bonds.index = pd.to_datetime(data_bonds.index, format='%d.%m.%Y')

data_bonds.index = pd.to_datetime(data_bonds.index, format='%Y-%m-%d')
data_bonds["Último"] =data_bonds["Último"].str.replace(',', '').astype(float)/100000.0000
df = data_bonds[start_date:end_date]

df= data_bonds["Último"]





# Define the base time-series chart.
def get_chart(data):
    hover = alt.selection_single(
        fields=["Date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Evolución de Retornos Acumulados Indices y Commodities")
        .mark_line()
        .encode(
            x=alt.X("Date", title="Fecha"),  # Cambia el nombre del eje X
            y=alt.Y("Retorno Acumulado", title="% Ret. Acum"),  # Cambia el nombre del eje Y,
            color="symbol:N",  # Añadir ":N" para indicar que es una variable nominal
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="yearmonthdate(Date)",
            y="Retorno Acumulado",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Date", title="Fecha"),
                alt.Tooltip("Retorno Acumulado", title="% Ret. Acum"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()





def get_chart_price(data):
    hover = alt.selection_single(
        fields=["Date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Evolución de Precios de Indices y Commodities")
        .mark_line()
        .encode(
            x=alt.X("Date", title="Fecha"),  # Cambia el nombre del eje X
            y=alt.Y("Adj Close", title="Precio (USD)"),  # Cambia el nombre del eje Y,
            color="symbol:N",  # Añadir ":N" para indicar que es una variable nominal
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="yearmonthdate(Date)",
            y="Adj Close",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Date", title="Fecha"),
                alt.Tooltip("Adj Close", title="Precio (USD)"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()

if not source.empty:
    
# Crear y mostrar el gráfico
    chart = get_chart(source)
    chart_price = get_chart_price(source)
    
    st.markdown("""---""")
    st.subheader("Evolucion de los Bonos")
    st.line_chart(df, use_container_width=True)
    st.subheader("Evolucion de los Indices y Commodities")

    st.altair_chart(chart, use_container_width=True)
    st.markdown("""---""")
    st.altair_chart(chart_price, use_container_width=True )
    st.markdown("""---""")

    
else:
    st.warning("No se sekeccionaron Acciones")
