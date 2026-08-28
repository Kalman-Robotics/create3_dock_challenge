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
>
> **⚠️ No alargar los textos.** Se midieron las cinco categorías ya publicadas
> en hrfest.org y estos son los límites reales por pestaña. Pasarse rompe la
> maqueta de la tarjeta:
>
> | Pestaña | Rango en el sitio | Nuestro |
> |---|---|---|
> | El Desafío / Bases | 439 – 1054 | 926 |
> | Entorno / Especificaciones | 410 – 969 | 573 |
> | **Evaluación** | **372 – 499** | 470 |
> | Premiaciones / Acreditaciones | 1054 – 1523 | 1064 |
> | Registrarse | 565 – 1192 | 684 |
>
> *(Caracteres de texto plano. La media del sitio es 794 y la mediana 848.)*

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

Lleva un **iRobot Create 3** de vuelta a su estación de carga usando únicamente
el LiDAR. El docking por infrarrojos que trae de fábrica —y la acción `/dock`
que lo resuelve en una línea— están prohibidos.

**El Reto:** El robot lleva un **LiDAR incorporado**, pero con él no ve el
dock. Justo encima de la estación hay **dos cajas separadas por un hueco**: ésa
es su referencia. Hay que escribir un nodo de ROS 2 que las detecte con el
LiDAR, calcule el centro del hueco —que es el eje del dock— y lleve al robot
hasta acoplarse.

**Prueba de Clasificación:** Repositorio público de GitHub con la solución, más
un video demostrativo de máximo 5 minutos.

**La Final:** El Top 8 despliega su código en un **iRobot Create 3 físico** y lo
ejecuta en vivo, desde una pose de arranque que no conoce.

**Beneficio:** todo equipo que complete el reto en simulación —entre o no al
Top 8— gana **acceso al laboratorio de Kalman Robotics** y un mes gratis de
nuestra plataforma.

📂 Guía técnica completa:
**https://github.com/Kalman-Robotics/create3_dock_challenge**

---

## 2 · Pestaña «Entorno»

**Plataforma:** iRobot Create 3 en **Gazebo Classic 11** sobre **ROS 2 Humble**
(Ubuntu 22.04, también WSL2 o Docker). Sin GPU dedicada.

**Sensor:** LiDAR Slamtec RPLIDAR C1 — 360°, 10 Hz, hasta 12 m.

**Marcador:** dos cajas de 8 × 8 × 12 cm separadas por un hueco de 9.5 cm. El
centro del hueco es el eje del dock.

**Lenguaje:** libre en ROS 2 — Python o C++.

**Hardware del participante:** ninguno. El robot físico lo pone Kalman Robotics.

**Prohibido:** la acción `/dock`, los sensores infrarrojos, el ground truth del
simulador y codificar posiciones fijas.

📂 Especificación completa en el repositorio.

---

## 3 · Pestaña «Evaluación»

El jurado **ejecuta la solución** en **3 corridas desde poses iniciales
sorteadas** que el equipo no conoce, con 180 segundos por corrida.

**50 % Acoplamiento:** que el robot quede acoplado. Sin acoplar, el resto
puntúa cero.

**25 % Tiempo:** promedio de las corridas exitosas.

**25 % Precisión:** error lateral y angular al acoplarse.

**Penalizan** los choques. **Descalifican** usar una interfaz prohibida o
codificar posiciones fijas.

**El podio se decide en la Gran Final**, sobre el robot real.

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

**Todos los que completen el reto:** Certificado de Reto Completado, **acceso al
laboratorio de Kalman Robotics** y **un mes gratis de la plataforma**, aunque no
entren al Top 8.

Las suscripciones a la plataforma son **individuales**: cada integrante del
equipo recibe la suya, hasta 3 por equipo.

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
| Equipos | Máximo 3 integrantes · también individual |
| Divisiones | Menores de 18 (exhibición) · Mayores de 18 (podio) |
| Cierre de envíos | 20 de septiembre de 2026, 23:59 (Perú) |
| Anuncio Top 8 | 30 de septiembre de 2026 |
| Gran Final | **Viernes 6 de noviembre de 2026, 14:00–16:00, Auditorio** |
| Cupo de la final | 8 equipos |
| Recursos necesarios en la final | 1 iRobot Create 3, 1 dock, 2 cajas marcadoras, mesa y proyector |

> La fecha coincide con la jornada central de competencias del congreso.

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
