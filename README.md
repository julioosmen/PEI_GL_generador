# 📘 Generador PEI Municipal (Prototipo)

Este prototipo permite a una municipalidad provincial o distrital del Perú completar las secciones básicas
del Plan Estratégico Institucional (PEI) y generar un archivo Word con la estructura estándar.

## Estructura
- `app.py`: aplicación principal de Streamlit.
- `modules/inputs.py`: formularios y lógica de recolección de datos.
- `modules/word_generator.py`: genera el documento `.docx` usando python-docx.
- `data/ejemplos.xlsx`: archivo con ejemplos referencia.
- `.streamlit/config.toml`: configuración de Streamlit.

## Requisitos
```bash
pip install -r requirements.txt
```

## Ejecutar localmente
```bash
streamlit run app.py
```

## Notas
- El documento Word generado es en **texto simple** (sin plantillas complejas) y se guarda como `PEI_[nombre_municipalidad].docx` al descargarse.
- Esta es una versión inicial; se pueden añadir validaciones, plantillas y guardado en la nube en próximas iteraciones.
