# 🛡️ Gobernanza de Datos

La gobernanza asegura la calidad, seguridad y trazabilidad del flujo de datos desde la ingesta hasta el análisis.

## 1️⃣ Origen y linaje de datos
- **Registro de fuentes:** Documentar para cada CSV el proveedor, frecuencia de actualización y responsable.  
- **Linaje:** Mantener metadatos que describan el camino desde el archivo crudo (RAW) hasta capas bronze y silver (transformaciones, reglas aplicadas, fecha de ejecución).  
- **Versionado:** Nombrar archivos con prefijo de fecha o commit (`raw_2025-09-01.csv`).

## 2️⃣ Validaciones mínimas
- **Esquema:** Columnas esperadas (`date`, `partner`, `amount`).  
- **Tipos de datos:** Fecha válida ISO, `partner` no vacío, `amount` numérico y > 0.  
- **Valores nulos y duplicados:** Rechazar o registrar incidencias.  
- **Integridad de negocio:** Fechas no futuras, montos dentro de rangos aceptables.

## 3️⃣ Política de mínimos privilegios
- Conceder acceso de lectura/escritura solo a quienes lo requieran según rol.  
- Mantener secretos (credenciales, tokens) fuera del repositorio.  
- Usar `.env` o almacenes seguros para contraseñas y claves.

## 4️⃣ Trazabilidad y auditoría
- Logs automáticos por cada ejecución del pipeline (usuario, fecha, resultado).  
- Historial de transformaciones y reglas aplicadas.  
- Identificadores de lote o ejecución para enlazar cada dataset con su origen.

## 5️⃣ Roles recomendados
| Rol                 | Responsabilidad principal                                         |
|---------------------|-------------------------------------------------------------------|
| **Data Engineer**    | Diseñar y mantener el pipeline ETL, controlar ingesta y validaciones. |
| **Data Steward**     | Supervisar calidad y cumplimiento de estándares.                  |
| **Analista de Datos**| Explorar datos en capa silver/gold, generar métricas y KPIs.       |
| **Administrador**    | Gestionar permisos, accesos y seguridad.                          |

> ✅ Estas pautas aseguran consistencia y protección de la información a lo largo de todo el ciclo de vida de datos.
