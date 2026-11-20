"""Public academic UI; inference uses the unchanged sealed portable models."""
from pathlib import Path
import base64
import json
import sys
from datetime import date
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
from bootstrap import ensure_runtime
ensure_runtime()
sys.path.insert(0, str(ROOT / 'bundle/work/fashionpulse_service'))
from service import Predictor

st.set_page_config(page_title='FashionPulse AI', page_icon='👗', layout='wide')
st.markdown('''<style>
.stApp {background:#faf8f4;color:#24212b}
.block-container {max-width:1180px;padding-top:2.5rem}
h1 {letter-spacing:-.055em;font-size:3.2rem!important;color:#30213f}
h2,h3 {letter-spacing:-.025em}
[data-testid="stForm"] {background:white;border:1px solid #e8e1ed;border-radius:18px;padding:1.6rem}
[data-testid="stMetric"] {background:#eee7f6;border-radius:14px;padding:1.4rem}
[data-testid="stMetricValue"] {color:#684293}
[data-testid="stBaseButton-primary"] {background:#7046a0;border-color:#7046a0}
</style>''', unsafe_allow_html=True)

@st.cache_resource
def predictor():
    return Predictor()

st.title('FashionPulse AI')
st.caption('Pronósticos de las primeras 12 semanas de una prenda por tienda')
st.info('Prototipo académico con VISUELLE2 histórico. No validado para ventas actuales en Colombia. Las cantidades no representan probabilidad de éxito ni rentabilidad.')
model = predictor()
meta = model.metadata()
tab_predict, tab_evidence, tab_about = st.tabs(['Analizar prenda', 'Resultados de evaluación', 'Acerca del proyecto'])
with tab_predict:
    st.write('Elige un objetivo, completa los atributos y genera un pronóstico. El modelo visual necesita una fotografía de la prenda.')
    objective = st.radio('Objetivo del pronóstico', ['total_12weeks', 'weekly_mae'], format_func=lambda x: {'total_12weeks':'Estimar el total de 12 semanas · modelo con imagen','weekly_mae':'Reducir el error semanal · mediana por categoría'}[x])
    if objective == 'weekly_mae':
        st.caption('Esta referencia utiliza solo la categoría. La fecha organiza las semanas; la fotografía y los demás atributos no cambian sus cantidades.')
    with st.form('forecast_form'):
        cols = st.columns(2)
        payload = {'objective': objective}
        for i, (key, label) in enumerate([('category','Categoría'), ('color','Color'), ('fabric','Tejido'), ('retail','Tienda histórica')]):
            options = meta['options'][key]
            with cols[i % 2]:
                payload[key] = st.selectbox(label, options, index=options.index(meta['example'][key]))
        with cols[0]:
            payload['season'] = st.text_input('Temporada (SS18 o AW18)', meta['example']['season'])
        with cols[1]:
            payload['release_date'] = st.date_input('Fecha de lanzamiento', date.fromisoformat(meta['example']['release_date']), min_value=date(2016,1,1), max_value=date(2100,12,31)).isoformat()
        photo = st.file_uploader('Fotografía PNG o JPEG (máximo 8 MB y 12 megapíxeles)', type=['png','jpg','jpeg'])
        use_example = st.checkbox('Probar el ejemplo histórico completo (reemplaza atributos y fotografía)', value=False)
        st.caption('La fotografía se procesa en memoria; esta aplicación no la incorpora al entrenamiento ni la guarda en un catálogo.')
        submitted = st.form_submit_button('Generar pronóstico', type='primary')
    if submitted:
        st.session_state.pop('forecast_result', None)
        try:
            if use_example:
                payload = dict(meta['example'], objective=objective)
            if objective == 'total_12weeks':
                if photo is None and not use_example:
                    raise ValueError('Sube una fotografía para utilizar el modelo visual.')
                if photo is not None and photo.size > 8_000_000 and not use_example:
                    raise ValueError('La fotografía supera los 8 MB.')
                image_bytes = (ROOT/'bundle/runtime/example.png').read_bytes() if use_example else photo.getvalue()
                payload['image_base64'] = base64.b64encode(image_bytes).decode('ascii')
            with st.spinner('Calculando con el modelo entrenado…'):
                result = model.predict(payload)
            st.session_state['forecast_result'] = {'result':result, 'inputs':{k:v for k,v in payload.items() if k != 'image_base64'}}
        except ValueError as exc:
            st.error(str(exc))
        except Exception:
            st.error('No se pudo completar el cálculo. Intenta de nuevo con una imagen PNG o JPEG válida.')
    if 'forecast_result' in st.session_state:
        saved = st.session_state['forecast_result']
        result = saved['result']
        st.subheader('Último pronóstico calculado')
        st.caption('Corresponde a los atributos que se muestran abajo. Si cambias el formulario, vuelve a generar el pronóstico.')
        st.metric('Total estimado en 12 semanas', f"{result['total_12weeks']:.2f} unidades")
        frame = pd.DataFrame(result['forecast']).rename(columns={'week':'Semana','start_date':'Inicio','end_date':'Fin','units':'Unidades'})
        st.line_chart(frame.set_index('Semana')['Unidades'])
        st.dataframe(frame, hide_index=True, use_container_width=True)
        st.download_button('Descargar pronóstico CSV', frame.to_csv(index=False).encode('utf-8-sig'), 'fashionpulse-pronostico.csv', 'text/csv')
        with st.expander('Atributos utilizados y modelo'):
            st.json(saved['inputs'])
            st.write('Modelo:', result['model'])
            st.write('Variables utilizadas:', ', '.join(result['used_features']))
        for warning in result['warnings']:
            st.warning(warning)
with tab_evidence:
    st.subheader('Prueba temporal de 2019')
    st.write('1.441 productos nuevos · 31.125 series prenda-tienda · 373.500 observaciones semanales. Los modelos se seleccionaron antes de abrir esta prueba y no se reentrenaron con ella.')
    metrics = pd.DataFrame([m for m in meta['evaluation'] if m['variant'] == 'A'])
    st.dataframe(metrics[['model','mae','mae_total_12weeks','volume_bias_pct']].rename(columns={'model':'Modelo','mae':'MAE semanal','mae_total_12weeks':'MAE total 12 semanas','volume_bias_pct':'Sesgo de volumen (%)'}), hide_index=True, use_container_width=True)
    st.write('MAE es el error absoluto medio: menor es mejor. El sesgo de volumen compara la suma pronosticada con la observada; un valor negativo indica subestimación.')
    st.write('En tres cortes históricos, las imágenes redujeron el MAE semanal un 0,16 % y el error del total un 0,32 % frente a los árboles con atributos. La mejora es pequeña y no demuestra superioridad estadística. La mediana obtuvo menor MAE semanal.')
    st.warning('La prueba de 2019 ya fue utilizada. No debe reutilizarse como prueba intacta para nuevas decisiones. Los valores negativos publicados se conservaron; su causa no está confirmada.')
with tab_about:
    st.subheader('Estimar ventas al lanzar una prenda')
    st.write('El proyecto estudia si una fotografía y los atributos disponibles al lanzamiento ayudan a estimar las primeras 12 semanas de ventas por tienda, cuando aún no hay historial del nuevo producto.')
    st.write('ResNet18 preentrenada y congelada extrae 512 características visuales. Se normalizan y reducen a 32 componentes mediante PCA ajustado solo en entrenamiento. ExtraTrees combina esos componentes con atributos. La referencia alternativa usa la mediana por categoría.')
    st.write('VISUELLE2 proviene de un minorista italiano y contiene 5.355 productos. Se excluyó una imagen corrupta. Sus resultados no representan automáticamente otros países, marcas o periodos.')
    st.markdown('[Fuente de VISUELLE2](https://humaticslab.github.io/forecasting/visuelle) · [Encoder ResNet18](https://huggingface.co/timm/resnet18.a1_in1k)')
    st.write('Daniel Esteban Hurtado Andrade · Juan David Peña Acosta')