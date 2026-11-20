# FashionPulse AI

Aplicación: https://fashionpulse-ai-algeo2.streamlit.app/

Autores: Daniel Esteban Hurtado Andrade y Juan David Peña Acosta.

## Uso

Abre la web, selecciona el objetivo y completa los atributos. Para probar sin una foto, marca «Probar el ejemplo histórico completo» y genera el pronóstico. El modelo visual reproduce aproximadamente 12,93 unidades; la mediana, 12,00. Para analizar una imagen propia, desmarca el ejemplo y sube PNG/JPEG de hasta 8 MB y 12 megapíxeles. Se muestran doce semanas y exportación CSV.

## Modelos y alcance

ResNet18 congelado produce 512 características. Normalización L2, PCA32 ajustado solo en entrenamiento y ExtraTrees combinan imagen y atributos. La mediana por categoría es una referencia alternativa. La elección se fijó usando tres cortes temporales anteriores a la evaluación final de 2019 (1.441 productos y 31.125 series).

No mide probabilidad de éxito, rentabilidad ni efecto de promociones. La mejora visual frente a árboles sin imagen fue pequeña. Datos históricos italianos, sin validación para ventas actuales en Colombia. Se conservaron los valores negativos publicados; no se atribuyen a devoluciones sin evidencia.

## Ejecución reproducible

Python 3.11. Instalar `pip install -r requirements.txt`, ejecutar `streamlit run app.py`. El primer arranque descarga los pesos públicos de ResNet18 de una revisión fija de Hugging Face y verifica SHA256. No requiere AWS ni claves de API. `runtime.zip` contiene clases Python, modelos propios, metadatos, ejemplo y métricas; se extrae al arrancar. Los modelos se verifican antes de cargarse. No se distribuyen ventas completas ni datos de clientes.

## Verificación al 20 de noviembre de 2026

Pasaron las pruebas locales del paquete y de la interfaz, incluyendo ambos objetivos y rechazo de imagen ausente. En la web pública se comprobó la inferencia del ejemplo visual con las mismas doce predicciones. La URL responde HTTP 200 con una sesión HTTP nueva sin credenciales. Pendiente completar la comprobación del selector de archivos, descarga efectiva en navegador, móvil y reactivación tras reposo; la automatización del navegador se interrumpió en las pruebas de archivos. No se presenta la entrega como completamente validada todavía.

## Alojamiento

Streamlit Community Cloud, Python 3.11. El profesor no necesita instalar software ni que el computador del autor esté encendido. El servicio gratuito puede hibernar y requerir reactivación del visitante; no hay garantía de disponibilidad inmediata permanente. No se crearon recursos AWS para este despliegue.

## Fuentes

- Skenderi, Joppi, Denitto, Scarpa y Cristani (2022). The Multi-Modal Universe of Fast-Fashion: The Visuelle 2.0 Benchmark. CVPR Workshops, 2241-2246. https://humaticslab.github.io/forecasting/visuelle
- Encoder: https://huggingface.co/timm/resnet18.a1_in1k (Apache-2.0 según su ficha). Revisión 491b427b45c94c7fb0e78b5474cc919aff584bbf.

Las imágenes y datos de terceros conservan sus derechos y atribución originales.
