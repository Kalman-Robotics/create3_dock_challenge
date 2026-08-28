# Gran Final — Create 3 Dock Challenge

**Viernes 06 de noviembre de 2026 · 14:00 – 16:00 · Auditorio**

Este documento describe la segunda mitad del reto: qué pasa después de la
clasificatoria. Si todavía estás resolviendo la simulación, lo que necesitas
está en el [README principal](../README.md) — vuelve aquí cuando la tengas.

---

## Lo que cambia: se acabó el simulador

La final **no se disputa en Gazebo**. Los 8 finalistas despliegan su código en
un **iRobot Create 3 físico** y lo ejecutan en vivo delante del jurado y del
público.

Mismo robot, mismo LiDAR, mismas cajas marcadoras. Pero el mundo real:

| En simulación | En el robot real |
|---|---|
| Ruido gaussiano limpio de 1 mm | Ruido real, reflejos, superficies que absorben el láser |
| Las ruedas giran lo que les mandas | Deslizamiento, alfombra, irregularidades del suelo |
| La odometría es casi perfecta | Deriva acumulada |
| El robot arranca donde tú decides | **Pose de arranque sorteada, que no conoces** |
| Puedes repetir mil veces | Tienes dos intentos y hay gente mirando |

> **Aquí se cobra la regla anti-hardcode.** Tu código corre sobre una escena que
> no has visto, en un robot que no es el del simulador. Una solución que percibe
> se adapta; una que memoriza coordenadas se queda parada delante del público.

---

## 🔧 Antes de la final: el laboratorio de Kalman Robotics

**Todo equipo que complete el reto en simulación antes del 20 de septiembre
obtiene acceso al laboratorio de Kalman Robotics** para preparar la final sobre
el Create 3 real: afinar el algoritmo, ajustar umbrales y comprobar cómo se
comporta su detección con un LiDAR físico, un dock físico y un suelo real.

**No hace falta entrar al Top 8 para obtenerlo.** Basta con resolver el reto.

No es un beneficio simbólico: es la diferencia entre llegar a la final con
código que solo ha visto un simulador y llegar con código ya probado en
hardware. El salto de simulación a robot real es la parte más dura, y este
acceso existe para que no la enfrentes por primera vez el día de la final.

**Cómo se agenda:** no tienes que gestionar nada por tu cuenta. La información
para reservar turno y los permisos de acceso **se enviarán por correo a los
equipos que completen la clasificatoria**, una vez cerrado el plazo.

---

## Formato de la final

Dos horas para ocho equipos:

| Momento | Duración |
|---|---|
| Briefing y sorteo de orden y de poses de arranque | 15 min |
| **Turno por equipo** (8 equipos) | 11 min cada uno |
| Deliberación y resultados | 15 min |

### Dentro de tu turno de 11 minutos

1. **Despliegue (4 min).** Clonas y compilas tu repositorio en el equipo de la
   organización, o traes tu propia laptop ya configurada. El cronómetro corre.
2. **Intento 1 (máx. 3 min).** El robot arranca desde la pose sorteada.
3. **Intento 2 (máx. 3 min).** Solo si el primero falló. Se puntúa el mejor.

Entre intentos puedes **ajustar parámetros**, pero **no reescribir el
algoritmo**: el código que despliegas es el que enviaste el 20 de septiembre, o
el que hayas afinado en el laboratorio de Kalman.

> 💡 **Con 4 minutos de despliegue, ven con la laptop lista.** Compilar un
> workspace desde cero delante del público es la forma más rápida de perder el
> turno.

---

## Cómo se puntúa la final — 100 puntos

| Criterio | Puntos | Detalle |
|---|---:|---|
| **Docking logrado** | **50** | 50 pts al primer intento · 30 pts al segundo · 0 si no acopla. |
| **Tiempo** | **20** | Desde la orden de inicio hasta que el robot queda acoplado. Menor tiempo, más puntos. |
| **Robustez en hardware** | **15** | Sin choques contra el dock, las cajas o el público. Comportamiento controlado, sin movimientos bruscos ni velocidades peligrosas. |
| **Sustentación técnica** | **15** | Explicación al jurado de cómo detectas la firma, y qué tuviste que cambiar al pasar de simulación a robot real. |

### Cómo se decide el podio

El puntaje final es **30 % clasificatoria + 70 % final**. La simulación te lleva
al escenario; el robot real decide quién gana.

---

## Asistencia

La asistencia presencial es **obligatoria** para disputar el podio y reclamar
los premios físicos. Quien clasifique y no asista recibe únicamente el
certificado digital de clasificación.

---

[← Volver al README principal](../README.md)
