# Ficha para la plataforma HRFEST 2026

Contenido listo para copiar en el formulario de la categoría en
[hrfest.org](https://hrfest.org/congress/2026/competitions). Sigue la estructura
de pestañas que usan las demás competencias.

> Todo el detalle técnico vive en el repositorio. Esta ficha es el resumen
> público; el enlace al repo es la fuente completa.

---

## Datos de cabecera

| Campo | Contenido |
|---|---|
| **Nombre** | Create 3 Dock Challenge |
| **Subtítulo** | Docking Autónomo por LiDAR |
| **Organiza** | Kalman Robotics |
| **Repositorio** | https://github.com/Kalman-Robotics/create3_dock_challenge |

---

## Pestaña: El Desafío

Lleva un robot **iRobot Create 3** de vuelta a su estación de carga usando
únicamente el LiDAR. El sistema de docking por infrarrojos que trae de fábrica
—y la acción `/dock` que lo resuelve en una línea— están prohibidos.

**El Reto:** Escribir un nodo de ROS 2 que, desde una posición arbitraria de la
sala, detecte dos cajas marcadoras montadas en la pared detrás del dock, deduzca
de ellas el eje de la estación y acople el robot hasta que `/dock_status`
reporte `is_docked: true`. El robot nunca ve el dock: ve el marcador.

**Prueba de Clasificación:** Repositorio público de GitHub con la solución, más
un video de máximo 5 minutos grabado en toma única, con la cámara del
participante encendida en miniatura, mostrando el código y la simulación
corriendo hasta el acoplamiento. **Estrictamente sin cortes de edición.**

**La Final:** El Top 8 despliega su código en un **iRobot Create 3 físico** y lo
ejecuta en vivo, desde una pose de arranque sorteada que no conocen.

**Beneficio adicional:** todo equipo que complete el reto en simulación —entre o
no al Top 8— obtiene acceso al laboratorio de Kalman Robotics para preparar la
final con el robot real.

---

## Pestaña: Especificaciones

**Plataforma:** iRobot Create 3 simulado en Gazebo Classic 11 sobre ROS 2 Humble
(Ubuntu 22.04, compatible con WSL2 y Docker). No se requiere GPU dedicada ni
hardware propio para la clasificatoria.

**Sensor:** Slamtec RPLIDAR C1 — 720 muestras, 360°, 10 Hz, alcance 0.15–12 m,
ruido gaussiano σ = 1 mm. Montado invertido (`yaw = 180°`), igual que en el
robot físico: `ranges[0]` no apunta al frente.

**Marcador:** dos cajas de 8 × 8 × 12 cm que sobresalen 8 cm de la pared,
separadas por un hueco libre de 9.5 cm, a una altura de 13 a 25 cm. El eje del
dock coincide con el centro del hueco.

**Interfaces permitidas:** `/scan`, `/cmd_vel`, `/tf`, `/odom`, `/imu`,
`/dock_status`, `/hazard_detection`.

**Interfaces prohibidas:** la acción `/dock`, las acciones de navegación del
fabricante, los sensores IR (`/ir_opcode`, `/ir_intensity`) y el ground truth
del simulador (`/sim_ground_truth_*`, `/gazebo/*`).

**Restricciones:** prohibido hardcodear la posición del dock o trayectorias
fijas; prohibido modificar el paquete base; un único comando de lanzamiento;
180 segundos por corrida.

---

## Pestaña: Evaluación

El jurado ejecuta la solución en **3 corridas** desde poses iniciales sorteadas
que el equipo no conoce, con los parámetros por defecto del escenario.

**50% Acoplamiento:** ~17 puntos por corrida que termine con `is_docked: true`
dentro de los 180 s. Criterio habilitante: sin acoplar, el resto puntúa cero.

**25% Tiempo:** promedio de las corridas exitosas. Máximo con ≤ 45 s, escala
lineal decreciente hasta 0 puntos en 180 s.

**25% Precisión:** error lateral y angular al acoplarse, medidos contra el
ground truth del simulador. Acoplarse torcido cuenta como éxito, pero puntúa
menos que entrar centrado y perpendicular.

**Penalizaciones:** −10 puntos por corrida al golpear cajas, dock o paredes.
**Descalifican:** usar una interfaz prohibida, hardcodear poses o trayectorias,
modificar el paquete base, que la solución no arranque con el comando
documentado, o entregar un video con cortes de edición.

**Desempate:** más corridas exitosas → menor tiempo promedio → menor error
lateral.

---

## Pestaña: Premiaciones

**1er Lugar:** Trofeo de Campeón, Certificado Físico, **Kit NEXUS completo**
(robot móvil diferencial con micro-ROS, encoders, IMU y LiDAR D500) y 3 meses de
suscripción Pro a la plataforma de Kalman Robotics.

**2do Lugar:** Medalla, Certificado Físico, **LiDAR Waveshare D500** (DTOF 360°,
0.03–12 m) y 3 meses de suscripción Pro.

**3er Lugar:** Medalla, Certificado Físico y 3 meses de suscripción Pro.

**Top 8 Finalistas:** Certificado Virtual de Clasificación y acceso al
laboratorio de Kalman Robotics.

Las suscripciones Pro son individuales: cada integrante del equipo premiado
recibe la suya, hasta 5 por equipo. El pozo de premios puede ampliarse con
aportes de patrocinadores.

---

## Pestaña: Acreditaciones

**Constancia de Participación:** para todo equipo con inscripción y envío
válido.

**Certificado de Reto Completado:** para todo equipo que logre al menos una
corrida con `is_docked: true` sin faltas descalificatorias. **Incluye acceso al
laboratorio de Kalman Robotics** para trabajar con el iRobot Create 3 físico,
independientemente de la posición en el ranking.

**Certificado Virtual de Finalista Global:** para los 8 equipos clasificados.

**Certificado Físico de Finalista:** para los finalistas que asistan
presencialmente a la Gran Final.

**Certificado de Podio:** para el 1er, 2do y 3er lugar, junto con los premios
correspondientes.

La asistencia presencial es obligatoria para disputar el podio. Quien clasifique
y no asista recibe únicamente el certificado digital.

---

## Pestaña: Registrarse

**Fase 1 — Inscripción.** Registra a tu equipo en la plataforma HRFEST y recibe
por correo tu Código Único de Competidor.

**Fase 2 — Envío.** Con ese código, sube: (1) el enlace a tu repositorio público
de GitHub indicando el hash del commit a evaluar, (2) el video demostrativo y
(3) su enlace público.

**Cierre: 20 de septiembre de 2026, 23:59 (hora de Perú).** Fecha impostergable.

📂 **Toda la especificación técnica, el escenario, la instalación y las pistas
están en el repositorio:**
**https://github.com/Kalman-Robotics/create3_dock_challenge**

---

## Texto corto (para tarjeta o listado)

> **Create 3 Dock Challenge** — Docking Autónomo por LiDAR
>
> Lleva un iRobot Create 3 de vuelta a su estación de carga usando únicamente
> el LiDAR. Sin infrarrojos, sin la acción `/dock`, sin atajos del simulador:
> detecta el marcador geométrico, deduce el eje del dock y acopla. Clasificatoria
> en simulación desde casa; la final, sobre el robot real.

---

## Versión en inglés (por si la plataforma la pide)

**The Challenge.** Bring an **iRobot Create 3** back to its charging dock using
the LiDAR alone. The factory infrared docking system —and the `/dock` action
that solves it in one line— are forbidden. Write a ROS 2 node that detects two
marker boxes on the wall behind the dock, infers the dock axis from them, and
docks the robot until `/dock_status` reports `is_docked: true`.

**Qualifier.** Public GitHub repository plus a 5-minute single-take video, webcam
on, showing code and simulation running through a successful dock. **Strictly no
edit cuts.**

**Finals.** The Top 8 deploy their code on a **physical iRobot Create 3** and run
it live from an undisclosed starting pose.

**Bonus.** Every team that completes the qualifier —Top 8 or not— gets lab access
at Kalman Robotics to prepare on the real robot.

**Full specification:** https://github.com/Kalman-Robotics/create3_dock_challenge

---

*Kalman Robotics · HRFEST 2026*
