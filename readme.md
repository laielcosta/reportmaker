# 📋 ReportMaker - Generador de Informes de Reparos

## 🎯 Descripción

**ReportMaker** es una aplicación de escritorio diseñada para generar informes técnicos de reparos de manera rápida y profesional. La herramienta traduce automáticamente del español al inglés y corrige errores gramaticales, facilitando la documentación de incidencias técnicas.

### ✨ Características Principales

- ✅ **Traducción automática** español → inglés
- ✅ **Corrección gramatical** automática
- ✅ **3 tipos de informes**: OPENED, REOPENED, VERIFIED
- ✅ **Numeración automática** en procedimientos
- ✅ **Exportación a Word** (.docx)
- ✅ **Interfaz moderna** y fácil de usar
- ✅ **Vista previa en tiempo real**
- ✅ **Scrollbars funcionales** en todos los campos

---

## 📦 Instalación

### Opción 1: Usar el Ejecutable (Recomendado)

1. Descarga el archivo `GeneradorInformesReparos.exe`
2. Haz doble clic para ejecutar
3. **No requiere instalación ni Python**

### Opción 2: Ejecutar desde Python

**Requisitos:**
- Python 3.8 o superior
- Librerías necesarias:

```bash
pip install deep-translator
pip install language-tool-python
pip install python-docx
```

**Ejecutar:**
```bash
python report_maker.py
```

---

## 🚀 Guía de Uso

### 1️⃣ Seleccionar Tipo de Reparo

En la parte superior del formulario, selecciona el tipo de informe:

- **OPENED**: Nuevo reparo detectado
  - Requiere: Summary, Equipment, Descripción, Procedimiento, Resultado Esperado
  
- **REOPENED**: El problema persiste
  - Requiere: Equipment, Descripción, Procedimiento
  - Nota: NO incluye Summary ni Resultado Esperado
  
- **VERIFIED**: Problema verificado/resuelto
  - Requiere: Equipment, Descripción
  - Formato especial: "The problem is VERIFIED in this version"

### 2️⃣ Completar los Campos

#### 📝 **Summary** (solo OPENED)
Breve resumen del problema en una línea.

**Ejemplo:**
```
El router pierde conexión cada 2 horas
```

#### 🖥️ **Equipment Information**
Información técnica del equipo. Puedes escribir en español, se traducirá automáticamente.

**Ejemplo:**
```
Nombre del equipo: Router ASKEY 5G
Modelo: RTF8115VW
Número de Serie: SN123456789
Versión Hardware: V1.0
Versión Software: 2.4.1
Versión Firmware: FW_2024_03
Código de País: ES
```

#### 📄 **Descripción**
Describe el problema detalladamente. Escribe en español, se traducirá automáticamente.

**Ejemplo:**
```
El equipo presenta desconexiones aleatorias cada 2 horas aproximadamente.
Los usuarios reportan pérdida de conectividad intermitente.
El problema ocurre principalmente durante horas pico.
```

#### 🔧 **Procedimiento** (OPENED y REOPENED)
Lista los pasos realizados. La numeración es automática.

**Cómo usar:**
1. Escribe el primer paso después del "1. "
2. Presiona **Enter** y se agregará automáticamente "2. "
3. Continúa escribiendo cada paso
4. Usa el botón "Reiniciar Numeración" si necesitas empezar de nuevo

**Ejemplo:**
```
1. Verificar logs del sistema
2. Reiniciar el router
3. Actualizar firmware a versión más reciente
4. Monitorear comportamiento por 24 horas
```

#### ✅ **Resultado Esperado** (solo OPENED)
Describe qué se espera lograr después de aplicar el procedimiento.

**Ejemplo:**
```
El router debe mantener conexión estable sin desconexiones.
Los usuarios no deben experimentar interrupciones de servicio.
```

#### 📎 **Attachments**
Lista de archivos adjuntos (opcional).

**Ejemplo:**
```
screenshot_error.png, router_logs.txt, network_analysis.xlsx
```

### 3️⃣ Generar el Informe

1. Haz clic en **"✨ Generar Informe"**
2. La aplicación:
   - ✅ Traduce todo al inglés
   - ✅ Corrige errores gramaticales
   - ✅ Formatea el texto correctamente
   - ✅ Muestra el resultado en la vista previa

### 4️⃣ Usar el Informe Generado

Tienes 3 opciones:

- **📋 Copiar**: Copia el informe al portapapeles para pegarlo donde necesites
- **📄 Exportar Word**: Guarda el informe como documento .docx con formato profesional
- **🗑️ Limpiar**: Borra la vista previa (no afecta el formulario)

---

## 📋 Ejemplos de Informes Generados

### Ejemplo 1: OPENED

**Entrada (español):**
- Type: OPENED
- Summary: Router pierde conexión cada 2 horas
- Equipment: Router ASKEY 5G, Modelo RTF8115VW
- Descripción: El equipo presenta desconexiones aleatorias
- Procedimiento: 
  1. Verificar logs
  2. Reiniciar router
- Expected: Conexión estable sin interrupciones

**Salida (inglés):**
```
OPENED

Summary: Router loses connection every 2 hours

[Equipment information]:

Equipment name: ASKEY 5G Router
Model: RTF8115VW

[Fault]:
The equipment presents random disconnections

[Procedure]:
1. Check logs
2. Restart router

[Expected]:
Stable connection without interruptions
```

### Ejemplo 2: REOPENED

**Salida:**
```
REOPENED
The problem continues, REOPENED in this version.

[Equipment information]:
...

[Fault]:
...

[Procedure]:
...
```

### Ejemplo 3: VERIFIED

**Salida:**
```
[Equipment information]:
...

The problem is VERIFIED in this version

(Descripción del problema)
```

---

## ⚙️ Funciones Detalladas

### 🌐 Traducción Automática

- **Motor**: Google Translate (deep-translator)
- **Dirección**: Español → Inglés (detecta automáticamente)
- **Campos traducidos**: 
  - Summary
  - Descripción/Fault
  - Procedimiento
  - Resultado Esperado
  - Equipment Information (campos específicos)

### ✏️ Corrección Gramatical

- **Motor**: LanguageTool
- **Idioma**: Inglés (en-US)
- **Correcciones**:
  - Ortografía
  - Gramática
  - Puntuación
  - Estilo

### 📊 Equipment Information

**Traducciones automáticas de campos comunes:**

| Español | Inglés |
|---------|--------|
| Nombre del equipo | Equipment name |
| Modelo | Model |
| Número de serie | Serial Number |
| Versión hardware | Hardware Version |
| Versión software | Software Version |
| Versión firmware | Firmware Version |
| Código de país | Country Code |
| Product ID | Product ID |

Si escribes otros campos, se traducirán automáticamente.

### 🔢 Numeración Automática

El campo **Procedimiento** tiene numeración inteligente:

- ✅ Presiona **Enter** para agregar un nuevo número
- ✅ La numeración se mantiene consistente
- ✅ Puedes editar cualquier línea sin romper la numeración
- ✅ Al generar, se renumeran automáticamente los pasos válidos

**Botón "Reiniciar Numeración":**
- Borra todo el contenido
- Reinicia el contador a "1."
- Útil para empezar de cero

### 📄 Exportación a Word

El archivo Word generado incluye:

- ✅ **Formato profesional** con estilos
- ✅ **Títulos en negrita** para secciones
- ✅ **Colores especiales**:
  - REOPENED: Rojo
  - VERIFIED: Verde
- ✅ **Nombre automático**: `Repair_TIPO_YYYYMMDD_HHMMSS.docx`

---

## 🎨 Interfaz de Usuario

### Panel Izquierdo (Formulario)
- **Scrollable**: Desplázate con la rueda del mouse
- **Campos expandibles**: Todos los campos de texto tienen scroll
- **Campos dinámicos**: Se muestran/ocultan según el tipo de reparo

### Panel Derecho (Vista Previa)
- **Actualización en vivo**: Muestra el resultado al generar
- **Scrollable**: Desplázate para ver informes largos
- **Copyable**: Copia directamente desde aquí

---

## 🛠️ Solución de Problemas

### ❌ Error: "Summary obligatorio para OPENED"
**Solución**: Completa el campo Summary antes de generar.

### ❌ Error: "Equipment Information requerido"
**Solución**: Todos los tipos de reparo necesitan información del equipo.

### ❌ Error: "Procedimiento obligatorio para OPENED"
**Solución**: Escribe al menos un paso en el procedimiento.

### ⚠️ La traducción no funciona
**Posible causa**: Sin conexión a internet
**Solución**: Verifica tu conexión. La traducción requiere internet.

### ⚠️ El texto no se corrige gramaticalmente
**Posible causa**: LanguageTool no se inicializó
**Solución**: El texto se traducirá pero sin corrección. Funcionalidad opcional.

### ⚠️ No puedo ver todo el texto
**Solución**: Usa las scrollbars en cada campo. Todos los campos de texto tienen scroll.

---

## 💡 Consejos de Uso

### ✅ Mejores Prácticas

1. **Escribe en español**: La aplicación traduce automáticamente
2. **Sé específico**: Incluye todos los detalles técnicos relevantes
3. **Usa el procedimiento numerado**: Facilita el seguimiento
4. **Revisa la vista previa**: Verifica el resultado antes de copiar/exportar
5. **Guarda regularmente**: Usa "Exportar Word" para guardar copias

### 📝 Formato de Equipment

**Formato recomendado:**
```
Campo: Valor
Campo: Valor
...
```

**Evita:**
- Mezclar formatos
- Líneas sin estructura
- Información duplicada

### 🎯 Descripción Efectiva

**Incluye:**
- ✅ Qué está fallando
- ✅ Cuándo ocurre
- ✅ Frecuencia del problema
- ✅ Impacto en usuarios
- ✅ Condiciones específicas

**Evita:**
- ❌ Descripciones vagas
- ❌ Información irrelevante
- ❌ Opiniones personales

---

## 🔄 Flujo de Trabajo Recomendado

```
1. Detectar problema
   ↓
2. Seleccionar tipo (OPENED/REOPENED/VERIFIED)
   ↓
3. Completar información del equipo
   ↓
4. Describir el problema
   ↓
5. Documentar procedimiento (si aplica)
   ↓
6. Generar informe
   ↓
7. Revisar vista previa
   ↓
8. Copiar o Exportar
   ↓
9. Limpiar formulario para siguiente caso
```

---

## 🔐 Privacidad y Seguridad

- ✅ **Sin almacenamiento**: No guarda información localmente
- ✅ **Traducción en línea**: Usa Google Translate API (requiere internet)
- ✅ **Sin telemetría**: No envía datos de uso
- ⚠️ **Nota**: El texto se envía a servicios externos para traducción

---

## 📞 Soporte

Si encuentras problemas o tienes sugerencias:

1. Verifica esta documentación primero
2. Revisa la sección "Solución de Problemas"
3. Contacta al equipo de desarrollo

---

## 📝 Notas de Versión

### v1.0 (Actual)
- ✅ Scrollbars funcionales en todos los campos
- ✅ Interfaz mejorada con iconos
- ✅ Traducción automática
- ✅ Corrección gramatical
- ✅ 3 tipos de informes
- ✅ Exportación a Word
- ✅ Vista previa en tiempo real

---

## 🎓 Licencia

Este software es de uso interno. Todos los derechos reservados.

---

**¡Gracias por usar ReportMaker! 🚀**