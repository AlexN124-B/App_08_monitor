"""Monitor de estabilidad de una aplicación móvil: analiza descargas y caídas semanales."""

from typing import Final

# Añadid aquí las importaciones que necesitéis.
import logging
import sys

# ---------------------------------------------------------------------------
# Datos de la aplicación. Sustituid los del ejemplo APP-00 por los vuestros.
# ---------------------------------------------------------------------------
CODIGO: Final[str] = "APP-08"
NOMBRE: Final[str] = "Monitor de estabilidad"
# Una posición por semana, de la 1 a la 12. 0 descargas: app retirada.
DESCARGAS: Final = [1_200, 1_350, 1_280, 1_500, 0, 1_720,
                    2_050, 1_810, 1_980, 2_310, 2_200, 2_150]
CAIDAS: Final = [14, 12, 15, 9, 0, 22,
                 31, 8, 6, 9, 5, 4]

# ---------------------------------------------------------------------------
# Datos del programa. Solo hay que cambiar AUTORES.
# ---------------------------------------------------------------------------
VERSION_PROGRAMA: Final[str] = "1.0.0"
AUTORES: Final[str] = "Sebastian Stancu - Alejandro Nuñez"
PENDIENTE: Final[str] = "  (opción pendiente de implementar)"

# ---------------------------------------------------------------------------
# Constantes comunes.
# ---------------------------------------------------------------------------
PRIMERA_SEMANA: Final[int] = 1
ANCHO: Final[int] = 44
POR_MIL: Final[int] = 1_000
UMBRAL_ESTABLE: Final[float] = 5.0       # caídas por cada mil descargas
UMBRAL_ACEPTABLE: Final[float] = 10.0
UMBRAL_REVISAR: Final[float] = 15.0
OPCION_SALIR: Final[int] = 9

# ---------------------------------------------------------------------------
# Constantes de la pareja. Todo valor fijo del programa va aquí, con nombre.
# ---------------------------------------------------------------------------


MAX_SEMANAS_PREVISION: Final[int] = 104


# ---------------------------------------------------------------------------
# Excepciones propias de la pareja. Aquí va SemanaNoValida (opción 7).
# ---------------------------------------------------------------------------

class SemanaNoValida(Exception):
    """La semana consultada no es un número de semana válido."""
# ---------------------------------------------------------------------------
# Funciones auxiliares. tasa_caidas viene hecha; el resto, con su docstring,
# las completáis vosotros. No cambiéis sus cabeceras.
# ---------------------------------------------------------------------------
def tasa_caidas(descargas: int, caidas: int) -> float:
    """Devuelve las caídas por cada mil descargas.

    Lanza ZeroDivisionError si la semana no tiene descargas.
    """
    return caidas / descargas * POR_MIL


def estado(descargas: int, caidas: int) -> str:
    """Devuelve el estado de una semana según su tasa de caídas.

    Es uno de estos textos: "Estable", "Aceptable", "Revisar", "Crítica" o
    "Mantenimiento", este último si la semana no tiene descargas.
    """
    if descargas == 0:
        return "Mantenimiento"
    tasa = tasa_caidas(descargas, caidas)
    if tasa < UMBRAL_ESTABLE:
        return "Estable"
    elif tasa < UMBRAL_ACEPTABLE:
        return "Aceptable"
    elif tasa < UMBRAL_REVISAR:
        return "Revisar"
    return "Crítica"


def pedir_entero(mensaje: str, minimo: int, maximo: int) -> int:
    """Pide un entero entre minimo y maximo hasta que sea válido.

    Si se escribe algo que no es un entero o está fuera de rango, avisa y
    lo vuelve a pedir.
    """
    while True:
        texto = input(mensaje)
        try:
            valor = int(texto)
        except ValueError:
            print(f" «{texto}» no es un número entero.")
            continue
        if minimo <= valor <= maximo:
            return valor
        print(f" Escribe un número entre {minimo} y {maximo}.")


def pedir_real(mensaje: str, minimo: float, maximo: float) -> float:
    """Pide un número real entre minimo y maximo hasta que sea válido.

    Si se escribe algo que no es un número o está fuera de rango, avisa y
    lo vuelve a pedir.
    """
    while True:
        texto = input(mensaje)
        try:
            valor = float(texto.replace(",", "."))
        except ValueError:
            print(f" «{texto}» no es un número.")
            continue
        if minimo <= valor <= maximo:
            return valor
        print(f" Escribe un número entre {minimo} y {maximo}.")


def semana_valida(texto: str) -> int:
    """Convierte el texto en un número de semana de los datos.

    Lanza SemanaNoValida si no es un entero o está fuera de rango.
    """
    try:
        semana = int(texto)
    except ValueError:
        raise SemanaNoValida(f"«{texto}» no es un número de semana") from None
    ultima_semana = len(DESCARGAS)
    if not PRIMERA_SEMANA <= semana <= ultima_semana:
        raise SemanaNoValida(
            f"la semana {semana} no existe: hay de {PRIMERA_SEMANA} a {ultima_semana}")
    return semana


def comprobar_datos() -> int:
    """Revisa los datos semanales y devuelve el número de errores.

    Registra cada error con logging.error y cada semana de mantenimiento
    con logging.warning.
    """
    errores = 0
    if len(DESCARGAS) != len(CAIDAS):
        logging.error("las listas tienen distinto número de semanas")
        errores += 1
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        if descargas < 0 or caidas < 0:
            logging.error("semana %d: valor negativo", semana)
            errores += 1
        elif descargas == 0:
            logging.warning("semana %d: sin descargas (mantenimiento)", semana)
        elif caidas > descargas:
            logging.error("semana %d: más caídas que descargas", semana)
            errores += 1
    return errores


# ---------------------------------------------------------------------------
# Menú y opciones. La opción 1 viene hecha y la 2 tiene dos errores.
# ---------------------------------------------------------------------------
def mostrar_menu() -> None:
    """Muestra el menu principal de la aplicacion"""
    print("=" * ANCHO)
    print("MONITOR DE APP-00 · Agenda Escolar".center(ANCHO))
    print("=" * ANCHO)
    print("1. Listado semanal")
    print("2. Resumen")
    print("3. Estabilidad por semana")
    print("4. Primera semana que alcanza un umbral")
    print("5. Mejor racha sin problemas")
    print("6. Previsión de crecimiento")
    print("7. Consultar una semana")
    print("8. Comprobar los datos")
    print("9. Salir")



def opcion_1_listado() -> None:
    """Muestra las descargas, las caídas y la tasa de cada semana."""
    print(f"{'Semana':>6}{'Descargas':>11}{'Caídas':>8}{'Tasa ‰':>9}")
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        try:
            tasa = f"{tasa_caidas(descargas, caidas):.1f}"
        except ZeroDivisionError:
            tasa = "—"
        print(f"{semana:>6}{descargas:>11}{caidas:>8}{tasa:>9}")


def opcion_2_resumen() -> None:
    """Muestra los totales, la media y las semanas extremas."""
    total_descargas = 0
    total_caidas = 0
    activas = 0
    mas = 0
    semana_mas = 0
    menos = float("inf")
    semana_menos = 0
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        if descargas == 0:
            continue
        activas += 1
        total_descargas += descargas
        total_caidas += caidas
        if descargas > mas:
            mas = descargas
        semana_mas = semana
        if descargas < menos:
            menos = descargas
            semana_menos = semana
    media = total_descargas / activas
    tasa = tasa_caidas(total_descargas, total_caidas)
    print(f"Semanas activas:     {activas} de {len(DESCARGAS)}")
    print(f"Total de descargas:  {total_descargas}")
    print(f"Media semanal:       {media:.1f}")
    print(f"Más descargas:       semana {semana_mas} ({mas})")
    print(f"Menos descargas:     semana {semana_menos} ({menos})")
    print(f"Total de caídas:     {total_caidas}")
    print(f"Tasa global:         {tasa:.1f} ‰")


def opcion_3_estabilidad() -> None:
    """Muestra el estado de cada semana y cuántas semanas hay de cada estado."""
    estables = 0
    aceptables = 0
    revisar = 0
    criticas = 0
    mantenimiento = 0
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        estado_semana = estado(descargas, caidas)
        print(f"Semana {semana}: {estado_semana}")
        match estado_semana:
            case "Estable":
                estables += 1
            case "Aceptable":
                aceptables += 1
            case "Revisar":
                revisar += 1
            case "Crítica":
                criticas += 1
            case "Mantenimiento":
                mantenimiento += 1
    print("-" * ANCHO)
    print(f"Estables: {estables} · Aceptables: {aceptables} · Revisar: {revisar}")
    print(f"Críticas: {criticas} · Mantenimiento: {mantenimiento}")


def opcion_4_umbral() -> None:
    """Muestra la primera semana cuya tasa alcanza un umbral."""
    
    umbral = pedir_real("Umbral en caídas por mil: ", 0, 1000)

    for semana, (descargas, caidas) in enumerate(zip(DESCARGAS, CAIDAS), start=1):
        if descargas == 0:
            continue
        tasa = tasa_caidas(descargas, caidas)
        if tasa >= umbral:
            print(f"Primera semana: {semana} ({tasa:.1f} ‰)")
            break
    else:
        print(f"Ninguna semana alcanza {umbral:.1f} ‰")


def opcion_5_racha() -> None:
    """Muestra la mejor racha de semanas sin problemas."""

    mejor_inicio = 0
    mejor_longitud = 0

    inicio_actual = 0
    longitud_actual = 0

    for semana, (descargas, caidas) in enumerate(zip(DESCARGAS, CAIDAS), start=1):
        estado_semana = estado(descargas, caidas)

        if estado_semana in ("Estable", "Aceptable"):
            if longitud_actual == 0:
                inicio_actual = semana
            longitud_actual += 1

            if longitud_actual > mejor_longitud:
                mejor_longitud = longitud_actual
                mejor_inicio = inicio_actual
        else:
            longitud_actual = 0

    if mejor_longitud > 0:
        fin = mejor_inicio + mejor_longitud - 1
        print(
            f"Mejor racha: {mejor_longitud} semanas (de la {mejor_inicio} a la {fin})")
    else:
        print("No hay semanas sin problemas.")


def opcion_6_prevision() -> None:
    """Calcula cuándo se alcanza un objetivo de descargas."""

    for descargas in reversed(DESCARGAS):
        if descargas > 0:
            descargas_actuales = descargas
            break

    print(
        f"Descargas de la última semana activa: {descargas_actuales}")

    objetivo = pedir_entero("Objetivo semanal de descargas: ", descargas_actuales + 1, 1_000_000)

    crecimiento = pedir_real("Crecimiento semanal en %: ", 0.5, 50.0)

    semanas = 0
    descargas_previstas = float(descargas_actuales)

    while descargas_previstas < objetivo:
        semanas += 1
        descargas_previstas *= (1 + crecimiento / 100)

        if semanas > MAX_SEMANAS_PREVISION:
            print(f"No se alcanza en {MAX_SEMANAS_PREVISION} semanas.")
            break
    else:
        print(f"Se alcanza en {semanas} semanas ({descargas_previstas:.0f} descargas)")


def opcion_7_consulta() -> None:
    """Muestra los datos, el estado y la acción recomendada de una semana."""
    texto = input(f"Semana (1-{len(DESCARGAS)}): ")
    try:
        semana = semana_valida(texto)
    except SemanaNoValida as error:
        print(f" No se puede consultar: {error}")
        return
    for numero, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        if numero == semana:
            break
    estado_semana = estado(descargas, caidas)
    match estado_semana:
        case "Estable":
            accion = "Sin acciones"
        case "Aceptable":
            accion = "Vigilar en la próxima versión"
        case "Revisar":
            accion = "Revisar los informes de errores"
        case "Crítica":
            accion = "Publicar una versión correctora urgente"
        case "Mantenimiento":
            accion = "La app no estuvo publicada esa semana"
    print(f"Descargas: {descargas}")
    print(f"Caídas: {caidas}")
    print(f"Estado: {estado_semana}")
    print(f"Acción: {accion}")


def opcion_8_comprobar() -> None:
    """Comprueba los datos y muestra si son correctos."""
    errores = comprobar_datos()
    if errores == 0:
        print(f"Datos correctos: {len(DESCARGAS)} semanas")
    else:
        print("Los datos tienen errores: corrígelos antes de continuar.")


def main() -> None:
    """Ejecuta el menú principal del programa."""

    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)s: %(message)s"
    )

    errores = comprobar_datos()
    if errores > 0:
        sys.exit("Los datos tienen errores: corrígelos antes de continuar.")

    print(f"Monitor de estabilidad {VERSION_PROGRAMA} · {AUTORES}")
    try:
        while True:
            mostrar_menu()

            opcion = input("Opción: ")

            try:
                opcion = int(opcion)
            except ValueError:
                print(f"  «{opcion}» no es una opción.")
                continue

            match opcion:
                case 1:
                    opcion_1_listado()
                case 2:
                    opcion_2_resumen()
                case 3:
                    opcion_3_estabilidad()
                case 4:
                    opcion_4_umbral()
                case 5:
                    opcion_5_racha()
                case 6:
                    opcion_6_prevision()
                case 7:
                    opcion_7_consulta()
                case 8:
                    opcion_8_comprobar()
                case _ if opcion == OPCION_SALIR:
                    respuesta = input("¿Salir del programa? (s/n): ")
                    if respuesta.lower() == "s":
                        break
                case _:
                    print(f"Elige una opción entre 1 y {OPCION_SALIR}.")
    except KeyboardInterrupt:
        print("\nPrograma interrumpido.")

    print(f"Fin del monitor de {CODIGO}.")


if __name__ == "__main__":
    main()
