# Carga en la plataforma HRFEST 2026
## Categoría: Create 3 Dock Challenge

> **Para quien carga la información.**
> Cada bloque de este documento es **un campo de la plataforma**. Copiar y pegar
> tal cual, sin reescribir. Los textos ya están ajustados a la extensión que usan
> las demás categorías del congreso.
>
> - **Idioma:** esta versión es la de **español**. La versión en inglés va en
>   `FICHA_HRFEST_EN.md` (pendiente).
> - **Molde seguido:** el del *Smart Factory Challenge*, que es la otra categoría
>   de simulación. Mismas 5 pestañas, mismo orden.
> - **Regla de oro:** la ficha es un resumen. **Todo el detalle vive en el
>   repositorio**, y por eso el enlace se repite al cierre de varias pestañas.

---

## 0 · Identidad de la categoría

| Campo | Valor a cargar |
|---|---|
| **Nombre** | `Create 3 Dock Challenge` |
| **Subtítulo** | `Percepción y Navegación Autónoma` |
| **Organiza** | `Kalman Robotics` |
| **Enlace oficial** | `https://github.com/Kalman-Robotics/create3_dock_challenge` |
| **Imagen de fondo** | `docs/img/escenario.jpg` *(ver sección 7)* |
| **Icono** | `fa-robot` *(Font Awesome, como el resto de categorías)* |
| **Correo de contacto** | `alaurao@uni.pe` |

---

## 1 · Pestaña «El Desafío»

Lleva un robot **iRobot Create 3** de vuelta a su estación de carga usando
únicamente el LiDAR. El sistema de docking por infrarrojos que trae de fábrica
—y la acción `/dock` que lo resuelve en una sola línea— están prohibidos.

**El Reto:** El robot no puede ver el dock. Detrás de la estación hay dos cajas
marcadoras montadas en la pared, separadas por un hueco. Los equipos deben
escribir un nodo de ROS 2 que reconozca esa firma geométrica en el LiDAR,
deduzca de ella el eje del dock y acople el robot hasta que `/dock_status`
reporte `is_docked: true`.

**Prueba de Clasificación:** Repositorio público de GitHub con la solución, más
un video de máximo 5 minutos grabado en toma única, con la cámara del
participante encendida en miniatura, mostrando el código y la simulación
corriendo hasta el acoplamiento. **Estrictamente sin cortes de edición.**

**La Final:** El Top 8 despliega su código en un **iRobot Create 3 físico** y lo
ejecuta en vivo ante el jurado, desde una pose de arranque sorteada que no
conoce de antemano.

**Beneficio para todos los que lo logren:** todo equipo que complete el reto en
simulación —entre o no al Top 8— obtiene **acceso al laboratorio de Kalman
Robotics** para preparar la final con el robot real.

📂 Especificación completa, escenario, instalación y pistas:
**https://github.com/Kalman-Robotics/create3_dock_challenge**

---

## 2 · Pestaña «Entorno»

**Plataforma:** iRobot Create 3 simulado en **Gazebo Classic 11** sobre **ROS 2
Humble** (Ubuntu 22.04). Funciona en WSL2 y Docker: no hace falta formatear
Windows ni tener GPU dedicada.

**Sensor:** LiDAR **Slamtec RPLIDAR C1** — 360°, 720 muestras, 10 Hz, alcance de
0.15 a 12 m. Montado invertido sobre el robot, igual que en el equipo físico del
laboratorio.

**Marcador:** dos cajas de **8 × 8 × 12 cm** que sobresalen 8 cm de la pared,
separadas por un hueco libre de **9.5 cm**. El centro de ese hueco es el eje del
dock.

**Lenguaje:** libre dentro de ROS 2 — Python (`rclpy`) o C++ (`rclcpp`), con
librerías de terceros permitidas.

**Hardware del participante:** ninguno. La etapa clasificatoria es íntegramente
en simulación; el robot físico lo pone Kalman Robotics.

**Restricciones principales:** prohibido usar la acción `/dock`, los sensores
infrarrojos o el ground truth del simulador; prohibido codificar posiciones o
trayectorias fijas; prohibido modificar el paquete base.

📂 Lista completa de interfaces permitidas y prohibidas en el repositorio.

---

## 3 · Pestaña «Evaluación»

El jurado **ejecuta la solución** en **3 corridas desde poses iniciales
sorteadas** que el equipo no conoce, con los parámetros por defecto del
escenario y un límite de 180 segundos por corrida.

**50 % Acoplamiento:** puntos por cada corrida que termine con
`is_docked: true`. Es criterio habilitante: sin acoplar, el resto puntúa cero.

**25 % Tiempo:** promedio de las corridas exitosas. Puntaje máximo con 45
segundos o menos, decreciente hasta cero en 180 segundos.

**25 % Precisión:** error lateral y angular al acoplarse. Acoplarse torcido
cuenta como éxito, pero puntúa menos que entrar centrado y perpendicular.

**Penalizaciones:** −10 puntos por corrida al golpear las cajas, el dock o las
paredes.

**Descalifican:** usar una interfaz prohibida, codificar posiciones o
trayectorias fijas, modificar el paquete base, que la solución no arranque con
el comando documentado, o entregar un video con cortes de edición.

**Desempate:** más corridas exitosas → menor tiempo promedio → menor error
lateral de acoplamiento.

**El podio se decide 30 % con la clasificatoria y 70 % con la Gran Final** sobre
el robot real.

---

## 4 · Pestaña «Premiaciones»

**1er Lugar:** Trofeo de Campeón, Certificado Físico, **Kit NEXUS completo**
—robot móvil diferencial con micro-ROS, motores con encoders, IMU y LiDAR
D500— y **3 meses de suscripción Pro** a la plataforma de Kalman Robotics.

**2do Lugar:** Medalla, Certificado Físico, **LiDAR Waveshare D500** (DTOF 360°,
0.03 a 12 m) y **3 meses de suscripción Pro**.

**3er Lugar:** Medalla, Certificado Físico y **3 meses de suscripción Pro**.

**Top 8 Finalistas:** Certificado Virtual de Clasificación y **acceso al
laboratorio de Kalman Robotics**.

**Todos los que completen el reto:** Certificado de Reto Completado y **acceso
al laboratorio**, aunque no entren al Top 8.

Las suscripciones Pro son **individuales**: cada integrante del equipo premiado
recibe la suya, hasta 5 por equipo.

**Importante:** es obligatorio que los 8 finalistas asistan presencialmente a la
Gran Final para disputar el podio y reclamar los premios físicos. Quien
clasifique y no asista recibe únicamente el certificado digital.

*El pozo de premios puede ampliarse con aportes de patrocinadores.*

---

## 5 · Pestaña «Registrarse»

### Fase 1 · Inscripción de Equipo

Registra los datos de tu equipo y de su líder. Al finalizar recibirás un
**Código Único de Competidor** en tu correo, obligatorio para el siguiente paso.

> **Botón:** `Inscribir Equipo`

### Fase 2 · Envío de Entregables

Ingresa tu Código Único para validar tu equipo. Luego envía **el enlace a tu
repositorio público de GitHub**, indicando el hash del commit que quieres que se
evalúe, y **el enlace público de tu video demostrativo** en toma continua sin
edición.

> **Botón:** `Subir Evidencias`

**Cierre: 20 de septiembre de 2026, 23:59 (hora de Perú).** Fecha impostergable.

📂 Antes de empezar, revisa la guía técnica completa:
**https://github.com/Kalman-Robotics/create3_dock_challenge**

---

## 6 · Texto corto (tarjeta, listado y redes)

**Versión de una línea:**

> Lleva un robot de vuelta a su estación de carga usando únicamente el LiDAR.

**Versión de tarjeta (≈40 palabras):**

> **Create 3 Dock Challenge** — Percepción y Navegación Autónoma.
> Sin infrarrojos, sin la acción `/dock`, sin atajos del simulador: detecta el
> marcador geométrico, deduce el eje de la estación y acopla. Clasificatoria en
> simulación desde casa; la final, sobre el robot real.

**Versión para redes (≈220 caracteres):**

> 🤖 ¿Puedes hacer que un robot vuelva solo a su cargador usando nada más que un
> LiDAR? El sistema de fábrica está prohibido. Resuélvelo en simulación y gánate
> acceso a nuestro laboratorio para competir con el robot real.
> #HRFEST2026 #ROS2

---

## 7 · Recursos gráficos

La plataforma **no usa logos vectoriales**: cada categoría se ilustra con una
imagen de fondo y un icono de Font Awesome. Seguimos ese mismo patrón.

| Recurso | Archivo | Equivalente en otras categorías |
|---|---|---|
| **Imagen de fondo de la tarjeta** | `docs/img/escenario.jpg` | `smart-factory-bg.webp`, `minihumanoid_sumo.jpg` |
| **Icono de la categoría** | `fa-robot` | `fa-industry`, `fa-skull-crossbones`, `fa-running` |
| **Imagen del premio** | `docs/img/nexus_kit.jpg` | `factoryIO.jpg` del Smart Factory |
| **Trofeo** | *(usar el genérico del congreso)* | `trofeo_minihumanoid.jpg` |
| **Apoyo técnico** | `docs/img/planta_cotas.jpg` | — |

**Sobre el icono:** `fa-robot` está libre —ninguna otra categoría lo usa— y se
entiende de inmediato. Alternativa más específica: `fa-charging-station`, que
apunta justo al problema del reto.

Todos los archivos están en el repositorio, en `docs/img/`.

---

## 8 · Datos operativos (no van en la web, son para la organización)

| Dato | Valor |
|---|---|
| Equipos | Máximo 5 integrantes · también individual |
| Divisiones | Menores de 18 (exhibición) · Mayores de 18 (podio) |
| Cierre de envíos | 20 de septiembre de 2026, 23:59 (Perú) |
| Anuncio Top 8 | 30 de septiembre de 2026 |
| Gran Final | **Jueves 5 de noviembre de 2026, 14:00–16:00, Auditorio** |
| Cupo de la final | 8 equipos |
| Recursos necesarios en la final | 1 iRobot Create 3, 1 dock, 2 cajas marcadoras, mesa y proyector |

> ⚠️ **Verificar con HRFEST:** el cronograma general del congreso marca la Gran
> Final el **viernes 6**, pero esta categoría compite el **jueves 5**. Confirmar
> antes de publicar para que no haya dos fechas en circulación.

---

## 9 · Lista de verificación antes de publicar

- [ ] Nombre y subtítulo cargados
- [ ] Las 5 pestañas pegadas en orden
- [ ] Imagen de fondo subida e icono `fa-robot` asignado
- [ ] Enlace al repositorio activo en «El Desafío» y en «Registrarse»
- [ ] Botones de Fase 1 y Fase 2 enlazados a los formularios
- [ ] Fecha de la Gran Final confirmada con HRFEST
- [ ] Versión en inglés cargada
- [ ] Correo de contacto visible

---

*Kalman Robotics · HRFEST 2026*
