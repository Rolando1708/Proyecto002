# 002 - Introduction to Trading
 
## Descripción General
Este proyecto presenta el desarrollo, optimización y evaluación de una **estrategia de trading automatizada** aplicada al mercado de **criptomonedas**, específicamente sobre **Bitcoin (BTC/USDT)**.  
El objetivo es diseñar un modelo sistemático capaz de generar **rendimientos positivos y estables** en un entorno de alta volatilidad, minimizando el riesgo de sobreajuste y simulando condiciones de operación reales mediante **backtesting**, **optimización de hiperparámetros** y **análisis walk-forward**.
 
---
 
## Estructura del Proyecto
- **Introducción**  
  Plantea el contexto del mercado de criptomonedas y la necesidad de estrategias robustas y automatizadas. Explica el uso de **RSI**, **MACD** y **Bandas de Bollinger** como indicadores principales para capturar diferentes dimensiones del comportamiento del precio.
 
- **Estrategia**  
  La estrategia combina tres indicadores técnicos.  
  Se establece como condición que **al menos dos de los tres indicadores** coincidan para generar una señal de entrada o salida, reduciendo así señales falsas y aumentando la fiabilidad operativa.
  
  Indicadores utilizados:
  - **RSI (Relative Strength Index):** mide fuerza y velocidad del precio, identificando sobrecompra o sobreventa.  
  - **MACD (Moving Average Convergence Divergence):** detecta cambios en la tendencia del precio.  
  - **Bandas de Bollinger:** evalúan la volatilidad y posibles niveles de sobrevaloración o infravaloración.
 
- **Análisis de Datos**  
  Se empleó un dataset horario de Bitcoin.  
  Procesamiento previo:
  - Renombrar columna `Date` → `Datetime`.  
  - Reordenar registros de más antiguos a más recientes.  
  - Dividir datos en **train (60%)**, **test (20%)** y **validation (20%)**.  
  Esto permite evaluar el desempeño del modelo bajo distintos escenarios temporales y evitar el sobreajuste.
 
- **Metodología e Implementación**  
  - **Optimización de parámetros:**  
    Se usó **Optuna** para explorar combinaciones de hiperparámetros de RSI, MACD y Bandas de Bollinger.  
  - **Walk-Forward Analysis:**  
    Evalúa la estrategia en ventanas temporales consecutivas de entrenamiento y prueba, verificando su robustez y capacidad de generalización.  
  - **Backtesting:**  
    Simula el comportamiento histórico de la estrategia con condiciones realistas:
    - Comisión: **0.125%**
    - Capital inicial: **USD 1,000,000**
  - **Métricas utilizadas:**
    - **Sharpe Ratio:** rendimiento ajustado por volatilidad total.  
    - **Sortino Ratio:** rendimiento ajustado por riesgo negativo.  
    - **Maximum Drawdown:** pérdida máxima acumulada.  
    - **Calmar Ratio:** relación entre rentabilidad anual y pérdida máxima.
 
---
 
## Resultados Principales
 
### Parámetros Óptimos
| Parámetro | Valor |
|------------|-------|
| RSI Window | 13 |
| RSI Lower | 28 |
| RSI Upper | 70 |
| MACD Fast | 15 |
| MACD Slow | 20 |
| MACD Signal | 5 |
| BB Window | 18 |
| BB Dev | 2.4985 |
| Stop Loss | 0.0982 |
| Take Profit | 0.1445 |
| Capital Exposure | 0.2221 |
 
---
 
### Conjunto **Train**
| Métrica | Valor |
|----------|--------|
| **Sharpe** | 0.4613 |
| **Sortino** | 0.7092 |
| **Max Drawdown** | 50.55% |
| **Calmar** | 0.2646 |
| **Win Rate** | 52.96% |
| **Retorno total** | +56.08% |
 
El portafolio creció de $1,000,000 a $1,560,799.  
Se observan beneficios, aunque con una exposición elevada al riesgo.
 
---
 
### Conjunto **Test**
| Métrica | Valor |
|----------|--------|
| **Sharpe** | 0.9542 |
| **Sortino** | 1.4421 |
| **Max Drawdown** | 20.87% |
| **Calmar** | 1.3117 |
| **Win Rate** | 58.15% |
| **Retorno total** | +45.64% |
 
El desempeño mejora sustancialmente en riesgo-retorno, evidenciando buena generalización del modelo.
 
---
 
### Conjunto **Validation**
| Métrica | Valor |
|----------|--------|
| **Sharpe** | 0.3286 |
| **Sortino** | 0.4921 |
| **Max Drawdown** | 25.51% |
| **Calmar** | 0.3572 |
| **Win Rate** | 46.98% |
 
Rendimiento estable aunque con menor eficiencia. El portafolio final alcanzó **$1,584,860**, partiendo del capital del test.
 
---
 
### Conjunto **Test + Validation**
| Métrica | Valor |
|----------|--------|
| **Sharpe** | 0.6459 |
| **Sortino** | 0.9719 |
| **Max Drawdown** | 25.51% |
| **Calmar** | 0.7143 |
 
El rendimiento ajustado al riesgo es aceptable; el portafolio mantiene crecimiento sostenido con retrocesos moderados.
 
---
 
## Limitaciones
- Alta **volatilidad del mercado cripto**, generando resultados variables aun con datos históricos.  
- El **backtest** no incorpora todos los factores de un entorno operativo real (slippage, latencia, liquidez).  
- La estrategia, aunque rentable, muestra **sensibilidad a cambios de régimen** en el precio de Bitcoin.
 
---
 
## Conclusiones
La estrategia logró **rendimientos positivos y consistentes** considerando la complejidad del mercado de Bitcoin.  
Si bien las métricas de desempeño no son sobresalientes, permanecen dentro de un rango aceptable.  
El uso de **Optuna** y **walk-forward analysis** permitió reducir el sobreajuste y obtener resultados realistas.  
 
Se recomienda:
- Ampliar el número de indicadores.  
- Ajustar periodos de entrenamiento.  
- Implementar **validación cruzada temporal** y técnicas de aprendizaje adaptativo.
 
---
 
## Tecnologías y Herramientas
- **Lenguaje:** Python  
- **Librerías:**  
  - `pandas`, `numpy` — procesamiento de datos  
  - `optuna` — optimización de hiperparámetros  
  - `matplotlib` — visualización  
- **Frecuencia temporal:** 1 hora  
- **Activo:** BTC/USDT  
 
---
 
## Autores
**Luis Felipe Gómez Estrada**  
**Rolando Fortanell Canedo**  
Proyecto: *002 - Introduction to Trading*  
Fecha: *07 de octubre de 2025*  
Curso: *Microestructura y Sistemas de Trading*
