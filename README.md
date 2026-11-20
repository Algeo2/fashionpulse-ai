# FashionPulse AI - candidato a web pública

Autores: Daniel Esteban Hurtado Andrade y Juan David Peña Acosta.

Estado: preparación local; NO publicado ni validado en Community Cloud todavía.

## Ejecución

Usar Python 3.11. Desde esta carpeta:

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m streamlit run app.py
```

En Linux sustituir `.venv\Scripts\python` por `.venv/bin/python`.
La instalación necesita internet. Los pronósticos usan los modelos empaquetados,
sin descargar pesos ni leer la base original durante una consulta.

## Publicación pendiente

Subir esta carpeta a un repositorio dedicado. En Streamlit Community Cloud seleccionar
repositorio, rama, `app.py` y Python 3.11 en Advanced settings. La app no requiere
claves de AWS ni servicios de inferencia de pago. Configurar acceso público y probar
desde un navegador sin la sesión del propietario.

Community Cloud puede hibernar tras inactividad; el visitante puede reactivarlo.
No se promete disponibilidad continua ni rendimiento antes de medirlos en el servidor.

## Criterios de aceptación

- URL HTTPS pública que funcione con el computador del autor apagado.
- Consulta con imagen propia y referencia sin imagen; 12 semanas y CSV coincidentes.
- Sin permisos del propietario ni instalación para el profesor.
- Errores comprensibles con imagen ausente/inválida y fecha/temporada incorrectas.
- Prueba en escritorio y móvil, primera carga y reactivación tras reposo.
- Consumo de memoria y tiempo compatibles con el alojamiento gratuito.
- Solo resultados reales en las pantallas entregadas; limitaciones visibles.

## Datos y modelos

VISUELLE2: https://humaticslab.github.io/forecasting/visuelle
ResNet18: https://huggingface.co/timm/resnet18.a1_in1k
La carpeta bundle conserva el paquete académico sellado existente. No modificar
sus archivos sin regenerar la verificación; contiene una imagen histórica de prueba.
Antes de publicar el repositorio, revisar los archivos incluidos y la atribución de terceros.
No se incluye la base completa de ventas ni datos de clientes.
