import pandas as pd

def analizar_plan_completo(file_path):
    """
    Lee todas las hojas clave del archivo de plan estratégico hasta la hoja 5b
    y extrae matrices estratégicas para análisis posterior.
    """
    xls = pd.ExcelFile(file_path)
    hojas = [s for s in xls.sheet_names if s <= "5b"]

    resultados = {}
    for hoja in hojas:
        try:
            df = pd.read_excel(file_path, sheet_name=hoja)
            texto_plano = df.astype(str).fillna("").values.flatten()
            texto_consolidado = " ".join(texto_plano)
            resultados[hoja] = texto_consolidado[:2000]  # Limitamos a 2000 caracteres por hoja
        except Exception as e:
            resultados[hoja] = f"Error leyendo hoja: {e}"
    
    return resultados

def generar_diagnostico_preliminar(contenido_hojas):
    """
    Crea un resumen básico del contenido leído, útil para preprocesamiento con OpenAI o memoria.
    """
    resumen = []
    for hoja, texto in contenido_hojas.items():
        texto_lower = texto.lower()
        if "foda" in texto_lower:
            resumen.append(f"✅ Hoja {hoja} contiene análisis FODA")
        elif "pest" in texto_lower:
            resumen.append(f"✅ Hoja {hoja} contiene factores PEST")
        elif "canvas" in texto_lower:
            resumen.append(f"✅ Hoja {hoja} contiene elementos del modelo Canvas")
        elif "porter" in texto_lower or "fuerzas" in texto_lower:
            resumen.append(f"✅ Hoja {hoja} contiene análisis de Porter")
        elif "mckinsey" in texto_lower or "ge" in texto_lower:
            resumen.append(f"✅ Hoja {hoja} contiene matriz McKinsey")
        else:
            resumen.append(f"📄 Hoja {hoja} leída. Contenido general.")
    return resumen
