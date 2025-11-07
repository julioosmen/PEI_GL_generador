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
- Se ha creado un aplicativo denominado **"Generador del Plan Estratégico Institucional (PEI)"** que está disponible con el siguiente enlace: https://peiglgenerador.streamlit.app/. Actualmente el app permite seleccionar el código del pliego y una vez seleccionado se despliega el nombre, tipo, departamento, provincia y distrito. Luego, se dan opciones de las secciones del PEI (Misión, Objetivos Estratégicos Institucionales, Acciones Estratégicas Institucionales, Ruta Estratégica y Anexo B-2). 

Las secciones utilizan lo que está disponible en el archivo denominado "4.PEI matriz_formatos_v.24.10" que está el sharepoint de la DNCP. Más detalle: 

- Misión: se despliegan los 11 ejemplos de misión institucional para elegir uno de ellos. Además, se da un espacio para que se redacte considerando la estructura de redacción recomendada. 

- Objetivos Estratégicos Institucionales: se despliegan los 11 OEI de la matriz estandar para elegir uno o más. Una vez elegido los OEI, se muestra una tabla donde se consigna el código OEI, la denominación y su indicador. 

- Acciones Estratégicas Institucionales: esta sección depende de la anterior de OEI ya que una vez seleccionado los OEI, se ponen a disposición la lista de las AEI de la matriz estandar disponible según los OEI escogidos. De esta manera, el usuario podrá seleccionar las aei que deseen por cada OEI seleccionado. Finalmente, se mostrará una tabla donde se consigna el código OEI, código AEI, denominación del AEI y su indicador. 

- Ruta Estratégica: esta sección depende las anteriores (oei y aei) dado que una vez seleccionado los OEI y AEI respectivas, se mostrará una tabla con la vinculación OEI con la PGG y la vinculación AEI con la PGG.

- Anexo B-2: esta sección depende las anteriores (oei y aei) dado que una vez seleccionado los OEI y AEI respectivas, se mostrará una tabla con articulación de las AEI seleccionadas con las Políticas Nacionales.
