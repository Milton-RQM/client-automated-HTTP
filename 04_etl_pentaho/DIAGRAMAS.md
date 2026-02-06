# Diagramas de ETL - Pentaho Data Integration

## 📸 Cómo agregar tus imágenes de los diagramas

Este archivo contiene instrucciones para documentar visualmente tu transformación y job en Pentaho Spoon.

---

## 1. TRANSFORMACIÓN (t_load_kpi.ktr)

### Pasos en Pentaho Spoon:

1. **Abre Pentaho Spoon**
2. **Carga la transformación:** `04_etl_pentaho/t_load_kpi.ktr`
3. **Verifica que se vea completa en pantalla** (zoom si es necesario)
4. **Guarda una captura:** `Print Screen` → Pega en Paint/Gimp
5. **Guarda la imagen como:**
   ```
   04_etl_pentaho/diagramas/t_load_kpi.png
   ```

### Estructura esperada de la transformación:

```
CSV Input
    ↓
Select Values (opcional - renombra columnas)
    ↓
Type Casting (fecha, int, float)
    ↓
Filter Rows (validaciones)
    ↓
    ├─→ Table Output #1 → stg_kpi_endpoint_dia
    │
    └─→ Table Output #2 → fct_kpi_endpoint_dia
```

### Validaciones en "Filter Rows":

```
requests_total > 0 
AND p90_elapsed_ms >= avg_elapsed_ms
AND success_2xx + client_4xx + server_5xx <= requests_total
```

---

## 2. JOB (j_daily_kpi.kjb)

### Pasos en Pentaho Spoon:

1. **Abre Pentaho Spoon**
2. **Carga el job:** `04_etl_pentaho/j_daily_kpi.kjb`
3. **Verifica que se vea el flujo completo**
4. **Guarda una captura:** `Print Screen` → Pega en Paint/Gimp
5. **Guarda la imagen como:**
   ```
   04_etl_pentaho/diagramas/j_daily_kpi.png
   ```

### Estructura esperada del job:

```
[Inicio]
    ↓
[Ejecutar Transformación: t_load_kpi.ktr]
    ↓
[Validar Éxito]
    ├─→ SI → [Verificar Integridad de Datos]
    │           ↓
    │       [Contar filas en stg_kpi]
    │           ↓
    │       [Contar filas en fct_kpi]
    │           ↓
    │       [Comparar conteos]
    │           ↓
    │       [Registrar auditoría]
    │           ↓
    │       [FIN - ÉXITO]
    │
    └─→ NO → [Registrar Error]
                ↓
            [Enviar notificación? (opcional)]
                ↓
            [FIN - ERROR]
```

---

## 3. Ubicación de imágenes

Todas las imágenes deben ir en:

```
04_etl_pentaho/
├── diagramas/
│   ├── t_load_kpi.png          ← Transformación
│   ├── j_daily_kpi.png          ← Job
│   └── DIAGRAMAS.md             ← Este archivo
├── t_load_kpi.ktr
├── j_daily_kpi.kjb
└── schema.sql
```

---

## 4. Cómo actualizar el README.md

Una vez que tengas tus imágenes, actualiza el README.md:

**Busca esta sección:**

```markdown
### 📸 Diagramas de ETL (Pentaho)

**1. Transformación (t_load_kpi.ktr):**

```
[Espacio para agregar captura de Spoon]
```

**Reemplázalo por:**

```markdown
### 📸 Diagramas de ETL (Pentaho)

**1. Transformación (t_load_kpi.ktr):**

![Transformación t_load_kpi](04_etl_pentaho/diagramas/t_load_kpi.png)

**2. Job (j_daily_kpi.kjb):**

![Job j_daily_kpi](04_etl_pentaho/diagramas/j_daily_kpi.png)
```

---

## 5. Tips para mejores capturas

✅ **Haz zoom OUT** en Spoon para que todo quepa en pantalla
✅ **Maximiza la ventana** de Spoon antes de capturar
✅ **Usa pantallas de alta resolución** si es posible
✅ **Captura el área de trabajo** sin los menús superiores
✅ **Nombra archivos claramente** (t_load_kpi.png, j_daily_kpi.png)

❌ No captures ventanas emergentes o diálogos
❌ No capturaes con barras de herramientas visibles
❌ No uses nombres genéricos (screenshot1.png, screenshot2.png)

---

## Requisitos previos

- ✓ Pentaho Spoon instalado y funcionando
- ✓ Haber creado la transformación t_load_kpi.ktr
- ✓ Haber creado el job j_daily_kpi.kjb
- ✓ Conexión a SQLite configurada en Spoon
- ✓ Directorio `04_etl_pentaho/diagramas/` creado

---

## Validación

Después de agregar las imágenes:

1. Abre el README.md en tu navegador
2. Verifica que las imágenes se visualicen correctamente
3. Comprueba que los caminos sean relativos (`04_etl_pentaho/diagramas/...`)
4. Si no se ven, verifica que el directorio exista y los archivos .png estén allí

```bash
# Desde la raíz del proyecto:
dir 04_etl_pentaho\diagramas\
```

---

## Contacto / Preguntas

Si tienes dudas sobre cómo documentar los diagramas:
- Consulta la documentación de Pentaho: https://help.hitachivantara.com/
- Mira tutoriales de Spoon en YouTube
- Abre un issue en el repositorio

¡Tu documentación visual es fundamental para que otros entiendan el flujo! 📸✨
