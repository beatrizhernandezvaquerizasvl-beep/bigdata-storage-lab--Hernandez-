# 📑 Diccionario de Datos — Esquema Canónico

El **esquema canónico** define la estructura uniforme para consolidar datos heterogéneos en el almacén analítico.

| Campo    | Tipo        | Formato / Unidad | Descripción                                                     |
|----------|------------|------------------|-----------------------------------------------------------------|
| `date`   | `date`     | YYYY-MM-DD       | Fecha de la transacción o evento reportado.                     |
| `partner`| `string`   | Texto libre      | Identificador del socio, cliente o contraparte.                 |
| `amount` | `float`    | EUR              | Monto asociado a la transacción, expresado en euros.            |

---

## 🔄 Mapeos Origen → Canónico

Ejemplos de cómo campos heterogéneos se normalizan al esquema canónico:

| Dataset origen     | Campo origen         | Campo canónico | Transformación                                    |
|--------------------|---------------------|----------------|---------------------------------------------------|
| ventas_2023.csv    | fecha_operacion      | `date`         | Convertir a formato ISO `YYYY-MM-DD`.              |
| sales_raw.csv      | partner_name         | `partner`      | Normalizar texto (trim, upper/lower según regla).  |
| transacciones.csv  | importe_total        | `amount`       | Convertir a `float`, asegurar EUR (divisa única).  |
| pagos_clientes.csv | cliente              | `partner`      | Unificar identificadores; usar diccionario de IDs. |
| movimientos.xlsx   | fecha                | `date`         | Detectar formato `DD/MM/YYYY` y transformar a ISO. |
| ops_data.csv       | valor_eur            | `amount`       | Mapear a `float`, forzar dos decimales si aplica.  |

> 💡 Mantén un **catálogo de mapeos** actualizado para cada nueva fuente incorporada.

---

```markdown
