from dynamixel_sdk import PortHandler, PacketHandler
import time

# Configuración
DEVICE = "/dev/ttyUSB0"
BAUDRATE = 57600
PROTOCOL = 2.0
DXL_ID = 8

ADDR_OPERATING_MODE = 11
ADDR_TORQUE_ENABLE = 64
ADDR_GOAL_POSITION = 116
ADDR_PRESENT_POSITION = 132

POSITION_MODE = 3

MIN_DEG = 145.0
MAX_DEG = 198.54

TORQUE_OFF = 0
TORQUE_ON = 1


def deg_to_raw(deg):
    return round(deg * 4096 / 360)


def raw_to_deg(raw):
    return raw * 360 / 4096


port = PortHandler(DEVICE)
packet = PacketHandler(PROTOCOL)

try:
    # Abrir puerto
    if not port.openPort():
        raise RuntimeError("No se pudo abrir " + DEVICE)

    if not port.setBaudRate(BAUDRATE):
        raise RuntimeError("No se pudo establecer baudrate")

    print("Puerto conectado.")

    # Verificar modo de operación
    mode, result, error = packet.read1ByteTxRx(
        port, DXL_ID, ADDR_OPERATING_MODE
    )

    if result != 0 or error != 0:
        raise RuntimeError("No se pudo leer Operating Mode")

    print(f"Operating Mode: {mode}")

    if mode != POSITION_MODE:
        raise RuntimeError(
            "El servo no está en Position Mode. "
            "No se modificará automáticamente."
        )

    # Leer posición actual
    raw, result, error = packet.read4ByteTxRx(
        port, DXL_ID, ADDR_PRESENT_POSITION
    )

    if result != 0 or error != 0:
        raise RuntimeError("No se pudo leer Present Position")

    # Nos quedamos con la posición dentro de una vuelta
    raw_current = raw % 4096
    current_deg = raw_to_deg(raw_current)

    print(f"Posición actual: {current_deg:.2f}°")

    # Seguridad: primero Goal = posición actual
    packet.write4ByteTxRx(
        port,
        DXL_ID,
        ADDR_GOAL_POSITION,
        raw_current
    )

    # Ahora habilitamos torque
    packet.write1ByteTxRx(
        port,
        DXL_ID,
        ADDR_TORQUE_ENABLE,
        TORQUE_ON
    )

    print("Torque ON.")
    print(f"Rango permitido: {MIN_DEG}° - {MAX_DEG}°")

    # Pedir posición al usuario
    target = float(input("Posición objetivo en grados: "))

    if not MIN_DEG <= target <= MAX_DEG:
        raise ValueError(
            f"Posición fuera del rango seguro "
            f"({MIN_DEG}° - {MAX_DEG}°)"
        )

    goal_raw = deg_to_raw(target)

    packet.write4ByteTxRx(
        port,
        DXL_ID,
        ADDR_GOAL_POSITION,
        goal_raw
    )

    print(f"Moviendo ID 8 a {target:.2f}°")

    # Mostrar posición durante unos segundos
    for _ in range(20):
        raw, result, error = packet.read4ByteTxRx(
            port,
            DXL_ID,
            ADDR_PRESENT_POSITION
        )

        if result == 0 and error == 0:
            pos = raw_to_deg(raw % 4096)
            print(f"Actual: {pos:.2f}°")

        time.sleep(0.1)

finally:
    # Siempre apagar torque al terminar
    packet.write1ByteTxRx(
        port,
        DXL_ID,
        ADDR_TORQUE_ENABLE,
        TORQUE_OFF
    )

    port.closePort()
    print("Torque OFF. Puerto cerrado.")