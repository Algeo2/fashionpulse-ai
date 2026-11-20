# FashionPulse AI

Aplicación: https://fashionpulse-ai-algeo2.streamlit.app/

Autores: Daniel Esteban Hurtado Andrade y Juan David Peña Acosta.

## Uso

Abre la web y elige «Mi propia prenda». Selecciona categoría, color, tejido, tienda histórica, temporada y fecha, carga una foto PNG/JPEG (hasta 8 MB y 12 megapíxeles) y pulsa «Generar pronóstico». Se muestran la imagen utilizada, doce semanas, el total, CSV y una ficha JSON con los atributos y la huella de la imagen. «Ejemplo histórico» es un modo separado: reemplaza explícitamente imagen y atributos.

El precio opcional y la moneda sirven únicamente para un escenario aritmético de ingresos brutos (unidades × precio). No cambian la demanda estimada, no son variables del modelo y no estiman rentabilidad. No existe análisis de texto libre ni clasificación automática de los atributos. La fotografía debe corresponder a la categoría elegida.

## Modelos y alcance

ResNet18 congelado produce 512 características. Normalización L2, PCA32 ajustado solo en entrenamiento y ExtraTrees combinan imagen y atributos. La mediana por categoría es una referencia alternativa. La elección se fijó usando tres cortes temporales anteriores a la evaluación final de 2019 (1.441 productos y 31.125 series).

No mide probabilidad de éxito, rentabilidad ni efecto de promociones. La mejora visual frente a árboles sin imagen fue pequeña. Datos históricos italianos, sin validación para ventas actuales en Colombia. Se conservaron los valores negativos publicados; no se atribuyen a devoluciones sin evidencia.

## Ejecución reproducible

Python 3.11. Instalar `pip install -r requirements.txt`, ejecutar `streamlit run app.py`. El primer arranque descarga los pesos públicos de ResNet18 de una revisión fija de Hugging Face y verifica SHA256. No requiere AWS ni claves de API. `runtime.zip` contiene clases Python, modelos propios, metadatos, ejemplo y métricas; se extrae al arrancar. Los modelos se verifican antes de cargarse. No se distribuyen ventas completas ni datos de clientes.

## Verificación al 20 de noviembre de 2026

Pasaron las pruebas locales de los dos objetivos, imagen obligatoria, carga de bytes de una foto distinta, atributos propios, repetibilidad, rechazo de imagen corrupta, límite de tamaño y temporada inválida. Las consultas inválidas eliminan resultados previos. Duplicar el precio conserva las unidades y duplica solo el escenario de ingresos.

En producción se cargó un JPEG distinto mediante el selector de archivos, con el modo «Mi propia prenda» y categoría modificada. El resultado de prueba fue 12,7472884727803 unidades. Se descargaron CSV y JSON y se verificaron las doce semanas, suma, atributos y SHA256 de la foto contra el cálculo local. Esa prueba comprueba integración técnica, no exactitud comercial ni coherencia automática entre categoría e imagen. Se inspeccionaron formulario y resultado a 390 × 844 píxeles. Los ejemplos históricos siguen reproducibles (visual 12,93; mediana 12,00).

La URL responde HTTP 200 con sesión HTTP nueva sin credenciales. No se realizó una sesión completa de inferencia anónima, prueba de carga concurrente ni prueba del ciclo de hibernación. La revisión móvil fue de viewport, no en un teléfono físico.

## Alojamiento

Streamlit Community Cloud, Python 3.11. El profesor no necesita instalar software ni que el computador del autor esté encendido. El servicio gratuito puede hibernar y requerir reactivación del visitante; no hay garantía de disponibilidad inmediata permanente. No se crearon recursos AWS para este despliegue.

## Fuentes

- Skenderi, Joppi, Denitto, Scarpa y Cristani (2022). The Multi-Modal Universe of Fast-Fashion: The Visuelle 2.0 Benchmark. CVPR Workshops, 2241-2246. https://humaticslab.github.io/forecasting/visuelle
- Encoder: https://huggingface.co/timm/resnet18.a1_in1k (Apache-2.0 según su ficha). Revisión 491b427b45c94c7fb0e78b5474cc919aff584bbf.

Las imágenes y datos de terceros conservan sus derechos y atribución originales.
