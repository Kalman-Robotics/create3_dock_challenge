# Bases Oficiales — Kalman Dock Challenge

**Categoría oficial del HRFEST 2026 · Organiza: Kalman Robotics**

Documento normativo de la competencia. En caso de discrepancia con cualquier
otro material, **prevalece este documento** junto con las bases generales
publicadas en [hrfest.org](https://hrfest.org/congress/2026/competitions).

| | |
|---|---|
| **Versión** | 1.0 |
| **Vigencia** | Temporada HRFEST 2026 |
| **Cierre de envíos** | 20 de septiembre de 2026, 23:59 (hora de Perú) |
| **Gran Final** | Viernes 6 de noviembre de 2026, 14:00–16:00, Auditorio |

---

## Contenido

1. [Descripción de la competencia](#1-descripción-de-la-competencia)
2. [Requisitos de participación](#2-requisitos-de-participación)
3. [Especificaciones técnicas](#3-especificaciones-técnicas)
4. [Reglamento](#4-reglamento)
5. [Sistema de evaluación](#5-sistema-de-evaluación)
6. [Entregables y acreditación](#6-entregables-y-acreditación)
7. [Premios y reconocimientos](#7-premios-y-reconocimientos)
8. [Cronograma oficial](#8-cronograma-oficial)
9. [Disposiciones generales](#9-disposiciones-generales)

---

## 1. Descripción de la competencia

### 1.1 Objetivo

Desarrollar un nodo de ROS 2 capaz de llevar un robot móvil **iRobot Create 3**
desde una posición arbitraria hasta su estación de carga, y acoplarlo,
utilizando **exclusivamente un sensor LiDAR 2D** como fuente de percepción del
entorno.

El sistema de docking por infrarrojos que el fabricante provee de serie queda
**expresamente prohibido**. El participante debe resolver el problema desde
cero: detección de una firma geométrica en el entorno, estimación de pose
relativa y control de aproximación.

### 1.2 Fundamento

El reto reproduce un problema real de la robótica de servicio: recuperar la
autonomía energética de una plataforma cuando el fabricante no expone un
sistema de docking, o cuando este resulta insuficiente. La solución canónica
—marcador geométrico conocido + sensor de rango + control realimentado— es la
misma que emplean robots de almacén, hospitalarios y de limpieza profesional.

### 1.3 Modalidad

La competencia se desarrolla en **dos etapas**:

| Etapa | Modalidad | Plataforma |
|---|---|---|
| **Clasificatoria** | Remota, asincrónica | Simulación (Gazebo Classic 11) |
| **Gran Final** | Presencial, en vivo | iRobot Create 3 físico |

Clasifican a la Gran Final los **8 equipos** con mayor puntaje en la etapa
clasificatoria.

---

## 2. Requisitos de participación

### 2.1 Conformación de equipos

| Aspecto | Norma |
|---|---|
| Integrantes | De **1 a 3 personas** |
| Procedencia | Libre. Se admiten equipos multidisciplinarios y multiinstitucionales |
| Inscripción | Un único registro por equipo, a través del líder designado |
| Cambios de plantel | No se admiten después del cierre de inscripciones |

### 2.2 Divisiones por edad

Conforme a la política general del HRFEST:

| División | Edad | Carácter |
|---|---|---|
| **Escolar** | Menores de 18 años | Exhibición, aprendizaje y menciones de honor |
| **Universitaria / Profesional** | 18 años o más | Competencia oficial por el podio absoluto |

La edad se determina a la fecha de la Gran Final. Un equipo con al menos un
integrante mayor de edad compite en la división universitaria/profesional.

### 2.3 Requisitos técnicos del participante

Se requiere conocimiento operativo de:

- ROS 2 Humble (`rclpy` o `rclcpp`)
- Procesamiento de datos de sensores de rango (`sensor_msgs/LaserScan`)
- Transformaciones espaciales (`tf2`)
- Control de robots diferenciales

No se exige hardware propio para la clasificatoria. Los requisitos de máquina
figuran en la [sección 3.4](#34-requisitos-de-sistema).

---

## 3. Especificaciones técnicas

### 3.1 Plataforma robótica

**iRobot Create 3** (base mecánica Roomba serie i3), simulado mediante el
paquete oficial [`create3_sim`](https://github.com/iRobotEducation/create3_sim).

| Parámetro | Valor |
|---|---|
| Diámetro | 33.9 cm |
| Tracción | Diferencial, dos ruedas motrices |
| Velocidad máxima | 0.46 m/s (`safety_override: full`) |
| Frame base | `base_link` |
| Comando de velocidad | `/cmd_vel` (`geometry_msgs/Twist`) |

### 3.2 Sensor LiDAR

**Slamtec RPLIDAR C1**, montado sobre soporte de 16 × 11 × 6.5 cm fijado a la
tapa del robot, replicando el montaje físico del laboratorio.

| Parámetro | Valor |
|---|---|
| Tópico | `/scan` (`sensor_msgs/LaserScan`) |
| Frame | `laser_link` |
| Frecuencia de publicación | 10 Hz |
| Muestras por barrido | 720 (resolución angular 0.5°) |
| Rango angular | −π a +π (360°) |
| `angle_increment` | 0.0087388 rad |
| Alcance | 0.15 m – 12.0 m |
| Ruido gaussiano | σ = 1 mm |
| Altura del plano de escaneo | 0.1775 m sobre el suelo |
| **Orientación de montaje** | **Girado 180° (`yaw = 3.14`)** |

> **Advertencia normativa.** El LiDAR está montado invertido, igual que en el
> robot físico. `ranges[0]` **no** corresponde al frente del robot. La
> transformación correcta debe obtenerse vía TF (`base_link` ← `laser_link`).
> Esta característica se mantiene idéntica en la Gran Final.

### 3.3 Escenario y marcador

Sala cerrada de aproximadamente 6 × 4 m. La estación de carga se sitúa al pie
de una pared, centrada entre dos cajas marcadoras.

**Dimensiones del marcador** (constantes en clasificatoria y final):

| Medida | Valor |
|---|---|
| Cajas marcadoras | 8 × 8 × 12 cm |
| Protrusión respecto a la pared | 8 cm |
| Hueco libre entre cajas | 9.5 cm |
| Separación entre centros | 17.5 cm |
| Altura sobre el suelo | 13 cm a 25 cm |

**El eje de la estación de carga coincide con el centro del hueco entre las dos
cajas.** Esta es la única referencia geométrica que el participante puede
asumir como conocida.

### 3.4 Requisitos de sistema

| Componente | Especificación |
|---|---|
| Sistema operativo | Ubuntu 22.04 (nativo, WSL2 o Docker) |
| Distribución ROS | ROS 2 Humble Hawksbill |
| Simulador | Gazebo Classic 11 (no Ignition / Gazebo Sim) |
| Memoria RAM | 8 GB recomendado, 4 GB mínimo |
| Almacenamiento | 15 GB libres |
| GPU dedicada | No requerida |

---

## 4. Reglamento

### 4.1 Interfaces permitidas

| Interfaz | Tipo | Uso |
|---|---|---|
| `/scan` | `sensor_msgs/LaserScan` | Percepción del entorno |
| `/cmd_vel` | `geometry_msgs/Twist` | Comando de velocidad |
| `/tf`, `/tf_static` | `tf2_msgs/TFMessage` | Transformaciones entre frames |
| `/dock_status` | `irobot_create_msgs/DockStatus` | Verificación de acoplamiento |
| `/odom` | `nav_msgs/Odometry` | Odometría de ruedas |
| `/imu` | `sensor_msgs/Imu` | Unidad inercial |
| `/battery_state` | `sensor_msgs/BatteryState` | Estado de batería |
| `/hazard_detection` | `irobot_create_msgs/HazardDetectionVector` | Detección de colisión |

### 4.2 Interfaces prohibidas

El uso de cualquiera de las siguientes interfaces constituye **falta grave** y
conlleva descalificación inmediata:

| Interfaz | Motivo |
|---|---|
| Acción `/dock` | Constituye la solución al problema planteado |
| Acciones `/navigate_to_position`, `/drive_distance`, `/rotate_angle`, `/drive_arc`, `/wall_follow` | Comportamientos preexistentes del fabricante |
| `/ir_opcode`, `/ir_intensity` | Sistema de docking por infrarrojos |
| `/sim_ground_truth_pose`, `/sim_ground_truth_dock_pose` | Estado interno del simulador |
| `/gazebo/model_states`, `/gazebo/link_states`, servicios `/gazebo/*` | Estado interno del simulador |
| Frame TF `std_dock_link` | Referencia incorrecta en este escenario |

### 4.3 Prohibición de codificación rígida

Queda prohibido incorporar en el código:

- Coordenadas absolutas de la estación de carga o de las cajas marcadoras
- La pose inicial del robot
- Secuencias predeterminadas de movimiento no derivadas de la percepción

La solución debe **inferir** la ubicación del objetivo a partir de los datos del
LiDAR. Las dimensiones del marcador (sección 3.3) sí pueden emplearse como
conocimiento previo, por tratarse de propiedades del objeto a detectar y no de
su ubicación.

### 4.4 Integridad del paquete base

Queda prohibida toda modificación del paquete `create3_dock_challenge`
—incluidos mundo, URDF, archivos de lanzamiento, materiales y mallas—. La
solución debe residir en un paquete independiente.

La evaluación se ejecuta siempre con los **valores por defecto** de los
argumentos de lanzamiento.

### 4.5 Condiciones de ejecución

| Condición | Valor |
|---|---|
| Tiempo máximo por corrida | **180 segundos** |
| Comando de arranque | **Único**, documentado por el participante |
| Intervención manual durante la corrida | **No permitida** |
| Inicio de operación | Automático al lanzar el nodo |

### 4.6 Originalidad

El código debe ser de autoría original del equipo. Se permite y se recomienda
la consulta de literatura académica y documentación técnica, con la debida
citación. La reproducción de soluciones existentes a este mismo reto constituye
falta grave.

---

## 5. Sistema de evaluación

### 5.1 Condición de éxito

Una corrida se considera exitosa cuando el tópico `/dock_status` reporta
`is_docked: true` dentro del límite de 180 segundos, sin uso de interfaces
prohibidas y sin colisión con elementos del escenario.

**Criterio del simulador.** El acoplamiento se registra cuando se satisfacen
simultáneamente tres condiciones entre el emisor del dock y el receptor del
robot:

| # | Condición | Umbral |
|---|---|---|
| 1 | Distancia emisor–receptor | < 7.5 cm |
| 2 | Desviación del robot respecto al eje del dock | < 6° |
| 3 | Desviación de apuntamiento del robot hacia el dock | < 6° |

*(Constantes del simulador: `DOCKED_DISTANCE = 0.075 m`, `DOCKED_YAW = π/30`.)*

### 5.2 Protocolo de evaluación

El jurado ejecuta la solución del participante en **tres corridas
independientes**, desde poses iniciales sorteadas dentro de los siguientes
rangos y no comunicadas previamente:

```
x   ∈ [ 0.0,  1.3]  m
y   ∈ [−0.9,  0.9]  m
yaw ∈ [−π,    π  ]  rad
```

Todas las corridas emplean los parámetros por defecto del escenario, incluido
el ruido del LiDAR (σ = 1 mm).

### 5.3 Rúbrica de puntuación

**Puntaje total: 100 puntos.**

| Criterio | Puntos | Método de medición |
|---|---:|---|
| **Consecución del acoplamiento** | **50** | Aproximadamente 17 puntos por cada corrida finalizada con `is_docked: true` dentro del límite temporal. Criterio habilitante: sin acoplamiento, los demás criterios puntúan cero. |
| **Tiempo de ejecución** | **25** | Promedio de las corridas exitosas, medido desde el arranque hasta `is_docked: true`. Puntaje máximo con ≤ 45 s; escala lineal decreciente hasta 0 puntos en 180 s. |
| **Precisión de acoplamiento** | **25** | Error lateral (distancia del centro del robot al eje del dock) y error angular (desviación respecto a la perpendicular a la pared), medidos con el ground truth del simulador. |

### 5.4 Penalizaciones

| Falta | Sanción |
|---|---|
| Colisión con cajas, dock o paredes | −10 puntos por corrida |
| Uso de interfaz prohibida | **Descalificación** |
| Codificación rígida de poses o trayectorias | **Descalificación** |
| Modificación del paquete base | **Descalificación** |
| Solución que no compila o no arranca con el comando documentado | **Descalificación** |
| Video sin una corrida completa en toma continua | Se solicita reenvío |

### 5.5 Criterios de desempate

En orden de aplicación:

1. Mayor número de corridas exitosas
2. Menor tiempo promedio de acoplamiento
3. Menor error lateral de acoplamiento

### 5.6 Composición del jurado

La evaluación técnica corre a cargo del equipo de Kalman Robotics, con la
supervisión del comité organizador del HRFEST 2026. Las decisiones del jurado
son **inapelables**.

---

## 6. Entregables y acreditación

### 6.1 Procedimiento de inscripción

**Fase 1 — Registro del equipo.**
Realizar el registro en [hrfest.org](https://hrfest.org/congress/2026/competitions)
con los datos del equipo y de su líder. El sistema emite por correo electrónico
un **Código Único de Competidor**, obligatorio para la Fase 2.

**Fase 2 — Envío de entregables.**
Con el Código Único, remitir los tres entregables descritos a continuación.

### 6.2 Entregables obligatorios

#### 6.2.1 Repositorio de código

Repositorio público de GitHub —o carpeta pública de Drive— que contenga
**exclusivamente** el paquete de
solución del equipo. No debe incluir copias de `create3_dock_challenge`,
`create3_sim`, ni los directorios `build/`, `install/` o `log/`.

El archivo `README.md` del repositorio debe documentar:

- Nombres y correos electrónicos de todos los integrantes
- Instrucciones exactas de instalación y compilación
- **Comando único de lanzamiento** de la solución
- Descripción del algoritmo: detección del marcador, estimación del eje del
  dock, estrategia de aproximación y acoplamiento
- Limitaciones conocidas

Debe indicarse el **hash del commit** a evaluar. Los commits posteriores a la
fecha límite no se consideran.

#### 6.2.2 Video demostrativo

| Requisito | Especificación |
|---|---|
| Duración máxima | 5 minutos |
| Formato de grabación | La **corrida de docking** debe ir en toma continua. Fuera de ella se admite edición |
| Cámara del participante | Encendida en miniatura durante toda la grabación |
| Contenido mínimo | Simulación en ejecución y acoplamiento hasta `is_docked: true` |
| Contenido adicional | Código en pantalla con explicación verbal de la solución |
| Idioma | Español o inglés |

#### 6.2.3 Enlace público del video

URL accesible sin solicitud de permisos (YouTube, Google Drive o equivalente).

### 6.3 Verificación previa al envío

Se recomienda clonar el repositorio en un espacio de trabajo limpio y verificar
compilación y ejecución. **Una solución que no se ejecute en el entorno del
jurado no será evaluada.**

### 6.4 Acreditaciones y certificaciones

| Condición alcanzada | Acreditación |
|---|---|
| Inscripción y envío válido | Constancia de participación |
| **Al menos una corrida con `is_docked: true`** | **Certificado de Reto Completado** + acceso al laboratorio de Kalman Robotics + un mes gratis de la plataforma (por integrante) |
| Clasificación al Top 8 | Certificado virtual de Finalista Global |
| Asistencia presencial a la Gran Final | Certificado físico de Finalista |
| Podio (1.º, 2.º, 3.º) | Certificado físico + premios de la sección 7 |

> **Acceso al laboratorio.** La acreditación de reto completado habilita al
> equipo a preparar la Gran Final utilizando el iRobot Create 3 físico en las
> instalaciones de Kalman Robotics, con independencia de su posición en el
> ranking. Condiciones detalladas en [GRAN_FINAL.md](GRAN_FINAL.md).

### 6.5 Asistencia a la Gran Final

La asistencia presencial es **obligatoria** para los ocho equipos finalistas.
El podio se disputa únicamente entre los equipos presentes. Los equipos
clasificados que no asistan reciben exclusivamente el certificado digital de
clasificación.

---

## 7. Premios y reconocimientos

| Puesto | Reconocimiento |
|---|---|
| **1.º** | Trofeo de Campeón · certificado físico · **Kit NEXUS completo** · 3 meses de suscripción Pro |
| **2.º** | Medalla · certificado físico · **LiDAR Waveshare D500** · 3 meses de suscripción Pro |
| **3.º** | Medalla · certificado físico · 3 meses de suscripción Pro |
| **Top 8** | Certificado virtual de clasificación · acceso al laboratorio |

**Suscripciones Pro:** se otorgan de forma individual a cada integrante del
equipo premiado, hasta un máximo de cinco por equipo.

**Kit NEXUS:** plataforma robótica móvil diferencial de Kalman Robotics
(14 × 10 × 8 cm), con controladora propia con micro-ROS integrado, motores con
encoders, IMU y LiDAR D500. Preparada para SLAM y navegación autónoma.

**LiDAR Waveshare D500:** sensor DTOF 360°, rango 0.03–12 m, frecuencia de
muestreo 5000 Hz, resolución angular ≤ 0.72°, interfaz UART a 230400 bps.

> El pozo de premios puede ampliarse mediante aportes de patrocinadores. La
> fuente vinculante es [hrfest.org](https://hrfest.org/congress/2026/competitions).

---

## 8. Cronograma oficial

| Hito | Fecha |
|---|---|
| Apertura de inscripciones | 2 de julio de 2026 |
| **Cierre de envíos** | **20 de septiembre de 2026, 23:59 (hora de Perú)** |
| Publicación de resultados (Top 8) | 30 de septiembre de 2026 |
| **Gran Final presencial** | **viernes 6 de noviembre de 2026, 14:00–16:00, Auditorio** |

La fecha de cierre es **impostergable** conforme al cronograma general del
HRFEST 2026. No se contemplan prórrogas.

---

## 9. Disposiciones generales

### 9.1 Aceptación de las bases

La inscripción en la competencia implica la aceptación íntegra de este
reglamento y de las bases generales del HRFEST 2026.

### 9.2 Propiedad intelectual

Los participantes conservan la titularidad de su código. Al inscribirse,
autorizan a la organización a difundir su solución con fines educativos y de
divulgación, con reconocimiento de autoría.

### 9.3 Conducta

Se espera conducta ética y respetuosa en toda comunicación e interacción. La
organización se reserva el derecho de excluir a participantes que incurran en
plagio, suplantación o conducta inapropiada.

### 9.4 Modificaciones

La organización podrá introducir precisiones a este documento para aclarar
ambigüedades o corregir errores. Toda modificación se comunicará por los
canales oficiales y no alterará los criterios de evaluación una vez abierto el
periodo de envíos.

### 9.5 Casos no previstos

Las situaciones no contempladas en este reglamento serán resueltas por el
comité organizador, cuya decisión es inapelable.

---

## Contacto

| | |
|---|---|
| **Organiza** | Kalman Robotics |
| **Evento** | HRFEST 2026 |
| **Bases generales y registro** | https://hrfest.org/congress/2026/competitions |
| **Consultas técnicas** | Issues del repositorio del reto |
| **Correo** | alaurao@uni.pe |

---

## Documentos relacionados

| Documento | Contenido |
|---|---|
| [README principal](../README.md) | Guía técnica completa del reto: instalación, escenario, pistas |
| [GRAN_FINAL.md](GRAN_FINAL.md) | Detalle de la etapa presencial y del acceso al laboratorio |

---

*Documento normativo · Kalman Dock Challenge · HRFEST 2026 · Kalman Robotics*
