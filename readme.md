# 📋 ReportMaker v1.1 - Generador de Informes de Reparos

## 🎯 Descripción

**ReportMaker** es una aplicación de escritorio moderna diseñada para generar informes técnicos de reparos de manera rápida y profesional. La herramienta traduce automáticamente del español al inglés y corrige errores gramaticales, facilitando la documentación de incidencias técnicas.

### ✨ Características Principales v1.1

- ✅ **Diseño moderno estilo Windows 11** con bordes redondeados
- ✅ **Traducción automática** español → inglés
- ✅ **Corrección gramatical** automática
- ✅ **3 tipos de informes**: OPENED, REOPENED, VERIFIED
- ✅ **Numeración automática** en procedimientos
- ✅ **Exportación a Word** (.docx)
- ✅ **Interfaz moderna** con colores Windows 11
- ✅ **Vista previa en tiempo real**
- ✅ **Scrollbars funcionales** mejorados
- ✅ **Navegación con Tab** entre campos
- ✅ **Deshacer/Rehacer** con Ctrl+Z / Ctrl+Y
- ✅ **Atajos de teclado** modernos

---

## 🆕 Novedades en v1.1

### 🎨 Diseño Moderno Windows 11
- **Bordes redondeados** en todos los elementos (6px radius)
- **Colores oficiales** de Windows 11 (#0078D4, #107C10)
- **Sombras sutiles** para mejor profundidad visual
- **Botones personalizados** con efectos hover
- **Transiciones suaves** al interactuar

### ⌨️ Navegación Mejorada
- **Tab**: Navega entre campos en orden lógico
- **Ctrl+Z**: Deshacer cambios en campos de texto
- **Ctrl+Y**: Rehacer cambios
- **Ctrl+S**: Generar informe (atajo rápido)
- **Ctrl+N**: Limpiar formulario
- **Ctrl+E**: Exportar a Word
- **Ctrl+C**: Copiar vista previa

### 🖱️ Interacción Intuitiva
- **Efectos hover** en todos los botones
- **Cursor hand** al pasar sobre elementos clicables
- **Scrollbars estilo Windows 11** más elegantes
- **Focus visual** mejorado en campos activos

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

**Navegación:**
- Presiona **Tab** para ir al siguiente campo
- Usa **Ctrl+Z** para deshacer

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

**Características:**
- ✅ Scrollbar funcional estilo Windows 11
- ✅ Deshacer/Rehacer con Ctrl+Z/Y
- ✅ Fuente monoespaciada (Consolas) para mejor legibilidad

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
4. Usa el botón "🔄 Reiniciar" si necesitas empezar de nuevo

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

**Opción 1: Botón**
- Haz clic en **"✨ Generar"**

**Opción 2: Atajo de teclado**
- Presiona **Ctrl+S**

La aplicación:
- ✅ Traduce todo al inglés
- ✅ Corrige errores gramaticales
- ✅ Formatea el texto correctamente
- ✅ Muestra el resultado en la vista previa

### 4️⃣ Usar el Informe Generado

Tienes 3 opciones:

- **📋 Copiar** (o Ctrl+C): Copia el informe al portapapeles
- **📄 Exportar** (o Ctrl+E): Guarda como documento .docx
- **🗑️ Limpiar**: Borra la vista previa

---

## ⌨️ Atajos de Teclado

| Atajo | Acción |
|-------|--------|
| **Tab** | Navegar al siguiente campo |
| **Ctrl+Z** | Deshacer cambios |
| **Ctrl+Y** | Rehacer cambios |
| **Ctrl+S** | Generar informe |
| **Ctrl+N** | Limpiar formulario (nuevo) |
| **Ctrl+E** | Exportar a Word |
| **Ctrl+C** | Copiar vista previa (cuando está enfocada) |
| **Enter** | Auto-numerar (en Procedimiento) |

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

### 🎨 Diseño Windows 11

**Colores:**
- Primary: `#0078D4` (Azul Windows 11)
- Success: `#107C10` (Verde Windows 11)
- Background: `#F3F3F3` (Gris claro)
- Text: `#1A1A1A` (Negro suave)

**Elementos:**
- Bordes redondeados: 6px
- Sombras sutiles para profundidad
- Efectos hover suaves
- Scrollbars estilo moderno

### 🔢 Numeración Automática

El campo **Procedimiento** tiene numeración inteligente:

- ✅ Presiona **Enter** para agregar un nuevo número
- ✅ La numeración se mantiene consistente
- ✅ Puedes editar cualquier línea sin romper la numeración
- ✅ Al generar, se renumeran automáticamente los pasos válidos
- ✅ Deshacer con **Ctrl+Z** funciona perfectamente

---

## 🛠️ Solución de Problemas

### ❌ Error: "Summary obligatorio para OPENED"
**Solución**: Completa el campo Summary antes de generar.

### ❌ Error: "Equipment Information requerido"
**Solución**: Todos los tipos de reparo necesitan información del equipo.

### ❌ Los atajos de teclado no funcionan
**Solución**: Asegúrate de que la ventana de la aplicación esté enfocada (activa).

### ⚠️ Ctrl+Z no funciona en un campo
**Solución**: Haz clic en el campo primero para darle foco, luego usa Ctrl+Z.

### ⚠️ La traducción no funciona
**Posible causa**: Sin conexión a internet
**Solución**: Verifica tu conexión. La traducción requiere internet.

---

## 💡 Consejos de Uso

### ✅ Mejores Prácticas

1. **Usa Tab para navegar**: Más rápido que el mouse
2. **Aprovecha Ctrl+S**: Genera sin tocar el botón
3. **Ctrl+Z es tu amigo**: No tengas miedo de experimentar
4. **Escribe en español**: La app traduce por ti
5. **Revisa la vista previa**: Siempre antes de exportar

### 📝 Navegación Eficiente

**Flujo recomendado con teclado:**
1. Selecciona tipo con mouse (una vez)
2. **Tab** → Summary → escribe
3. **Tab** → Equipment → escribe
4. **Tab** → Descripción → escribe
5. **Tab** → Procedimiento → escribe pasos
6. **Tab** → Expected → escribe
7. **Tab** → Attachments → escribe
8. **Ctrl+S** → Generar
9. **Ctrl+E** → Exportar

---

## 🎨 Interfaz de Usuario

### Panel Izquierdo (Formulario)
- **Header azul** con título y versión
- **Sección expandible** con scroll suave
- **Campos con bordes redondeados** (6px)
- **Botones con hover effects**
- **Navegación con Tab** optimizada

### Panel Derecho (Vista Previa)
- **Header verde** distintivo
- **Área de texto** con fuente monoespaciada
- **Botones de acción** en la parte inferior
- **Scrollbar moderna** estilo Windows 11

### Elementos Modernos
- ✅ Bordes redondeados en todo
- ✅ Sombras sutiles
- ✅ Colores Windows 11 oficiales
- ✅ Iconos emoji integrados
- ✅ Efectos hover en botones

---

## 🔄 Flujo de Trabajo Recomendado

```
1. Detectar problema
   ↓
2. Abrir ReportMaker
   ↓
3. Seleccionar tipo (OPENED/REOPENED/VERIFIED)
   ↓
4. Usar Tab para navegar por campos
   ↓
5. Escribir información (español OK)
   ↓
6. Ctrl+S para generar
   ↓
7. Revisar vista previa
   ↓
8. Ctrl+E para exportar o Ctrl+C para copiar
   ↓
9. Ctrl+N para limpiar y siguiente caso
```

---

## 🔐 Privacidad y Seguridad

- ✅ **Sin almacenamiento local**: No guarda información
- ✅ **Traducción en línea**: Usa Google Translate API (requiere internet)
- ✅ **Sin telemetría**: No envía datos de uso
- ⚠️ **Nota**: El texto se envía a servicios externos para traducción

---

## 📝 Notas de Versión

### v1.1 (Actual) - Diseño Moderno
- ✨ **NUEVO**: Diseño completo estilo Windows 11
- ✨ **NUEVO**: Bordes redondeados (6px) en todos los elementos
- ✨ **NUEVO**: Navegación con Tab entre campos
- ✨ **NUEVO**: Deshacer/Rehacer con Ctrl+Z/Y
- ✨ **NUEVO**: Atajos de teclado (Ctrl+S, Ctrl+N, Ctrl+E)
- ✨ **NUEVO**: Botones personalizados con efectos hover
- ✨ **NUEVO**: Scrollbars estilo Windows 11
- ✨ **NUEVO**: Colores oficiales de Windows 11
- ✨ **NUEVO**: Sombras sutiles para profundidad
- 🔧 **MEJORADO**: Interfaz más espaciosa y limpia
- 🔧 **MEJORADO**: Mejor organización visual

### v1.0
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

## 🙏 Agradecimientos

Desarrollado con atención al detalle y diseño moderno para mejorar la productividad del equipo.

---

**¡Gracias por usar ReportMaker v1.1! 🚀**

*Diseñado con 💙 siguiendo los estándares de Windows 11*