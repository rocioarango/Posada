import csv
from pathlib import Path

import pandas as pd
import streamlit as st

# ---------- CONFIGURACIÓN ----------
ARCHIVO_APORTES = Path("aportes.csv")

# Opciones y cupos máximos
OPCIONES = {
    1: {"nombre": "Alfajores",                 "max": 2},
    2: {"nombre": "Petipanes para todos",      "max": 1},
    3: {"nombre": "Empanaditas surtidas",      "max": 2},
    4: {"nombre": "Wafers o dulces",           "max": 2},
    5: {"nombre": "Chips / chifles / papitas", "max": 3},
    6: {"nombre": "Gaseosa grande",            "max": 3},
    7: {"nombre": "Bebida no alcohólica",      "max": 3},
    8: {"nombre": "Bebida alcohólica",         "max": 3},
    9: {"nombre": "Otro (especificar)",        "max": 2},
}

# Lista fija de participantes (menú desplegable)
PARTICIPANTES = [
    "Katherine Silvestre",
    "Marden Ferruzo",
    "Rocio Dominguez",
    "George Aliaga",
    "Janet Rivera",
    "Ana Raez",
    "Israel Juarez",
    "Luis Moreano",
    "Yessevel Calvo",
    "Yelitza Arias",
    "Eduardo Pinto",
    "Millary Antunez",
    "Manuel Reyes",
    "Vladimir Tucto",
    "Rocio Arango",
    "Axel Fuentes",
    "Camila Alva",
    "Ricardo Céspedes",
]

# ---------- FUNCIONES AUXILIARES ----------

def cargar_aportes():
    """Lee el archivo de aportes (si existe) y retorna un DataFrame."""
    if ARCHIVO_APORTES.exists():
        return pd.read_csv(ARCHIVO_APORTES, dtype=str)
    else:
        return pd.DataFrame(columns=["nombre", "opcion", "detalle"])


def guardar_aportes(df_aportes: pd.DataFrame):
    """Guarda los aportes en CSV."""
    df_aportes.to_csv(ARCHIVO_APORTES, index=False, encoding="utf-8")


def contar_cupos_usados(df_aportes: pd.DataFrame):
    """Cuenta cuántas veces se ha elegido cada opción."""
    usados = {num: 0 for num in OPCIONES.keys()}
    if not df_aportes.empty:
        for _, fila in df_aportes.iterrows():
            try:
                num = int(fila["opcion"])
                if num in usados:
                    usados[num] += 1
            except (ValueError, TypeError):
                continue
    return usados


# ---------- APP STREAMLIT ----------

def main():
    st.set_page_config(page_title="Aportes para la Posada Territorial 2025", page_icon="🎁")
    st.title("🎁 Aportes para la Posada Territorial 2025")

    st.write(
        "Elige qué vas a llevar para el encuentro. "
        "Cada opción tiene un **cupo máximo** para que no se repitan demasiado los aportes."
    )

    # Cargamos aportes actuales
    df_aportes = cargar_aportes()
    cupos_usados = contar_cupos_usados(df_aportes)

    # Mostrar resumen de opciones
    st.subheader("Opciones y cupos")
    tabla_opciones = []
    for num, info in OPCIONES.items():
        usados = cupos_usados[num]
        maximo = info["max"]
        estado = "LLENO" if usados >= maximo else "Disponible"
        tabla_opciones.append(
            {
                "N.º": num,
                "Opción": info["nombre"],
                "Usados": usados,
                "Máximo": maximo,
                "Estado": estado,
            }
        )
    st.table(pd.DataFrame(tabla_opciones))

    # Verificar si todo está lleno
    if all(cupos_usados[n] >= OPCIONES[n]["max"] for n in OPCIONES):
        st.warning("⚠️ Todas las opciones están llenas. ¡Ya no hay cupos disponibles!")
        if not df_aportes.empty:
            st.subheader("Listado de aportes registrados")
            st.dataframe(df_aportes, use_container_width=True)
        return

    st.markdown("---")

    # ----- Formulario para registrar nuevo aporte -----
    st.subheader("Registrar tu aporte")

    with st.form("form_aporte"):
        # Ahora el nombre se elige de una lista
        nombre = st.selectbox(
            "Selecciona tu nombre:",
            PARTICIPANTES,
        )

        # Selectbox con todas las opciones, indicando cupos
        def etiqueta_opcion(num):
            info = OPCIONES[num]
            usados = cupos_usados[num]
            maximo = info["max"]
            lleno = " – LLENO" if usados >= maximo else ""
            return f"{num}. {info['nombre']} ({usados}/{maximo}){lleno}"

        opcion_seleccionada = st.selectbox(
            "Elige la opción que vas a llevar:",
            options=list(OPCIONES.keys()),
            format_func=etiqueta_opcion,
        )

        detalle = ""
        # Campo extra si es "Otro"
        if opcion_seleccionada == 9:
            detalle = st.text_input("Describe brevemente qué vas a llevar (Otro):")

        enviado = st.form_submit_button("Registrar aporte ✅")

    # Procesar envío
    if enviado:
        # Validaciones
        if not nombre.strip():
            st.error("Por favor selecciona tu nombre.")
            return

        # Evitar que una persona registre dos veces
        if not df_aportes.empty and nombre in df_aportes["nombre"].values:
            st.error("Ya registraste tu aporte antes. Si necesitas cambiarlo, avisa a la organización.")
            return

        opcion = int(opcion_seleccionada)

        if opcion not in OPCIONES:
            st.error("La opción seleccionada no existe.")
            return

        if cupos_usados[opcion] >= OPCIONES[opcion]["max"]:
            st.error("Esa opción ya está llena, por favor elige otra.")
            return

        if opcion == 9 and not detalle.strip():
            st.error("Por favor describe qué vas a llevar en 'Otro'.")
            return

        # Agregar aporte
        nuevo = {
            "nombre": nombre.strip(),
            "opcion": str(opcion),
            "detalle": detalle.strip() if detalle else "",
        }

        df_aportes = pd.concat([df_aportes, pd.DataFrame([nuevo])], ignore_index=True)
        guardar_aportes(df_aportes)

        st.success(f"✅ Registrado: **{nombre}** llevará **{OPCIONES[opcion]['nombre']}**")
        if detalle:
            st.info(f"Detalle: {detalle}")

        # Recargar automáticamente para actualizar los cupos y la tabla
        st.rerun()

    # Mostrar listado de aportes
    if not df_aportes.empty:
        st.markdown("---")
        st.subheader("Aportes registrados hasta ahora")
        # Mostrar también el nombre de la opción en texto
        df_mostrar = df_aportes.copy()
        df_mostrar["opcion_desc"] = df_mostrar["opcion"].astype(int).map(
            {k: v["nombre"] for k, v in OPCIONES.items()}
        )
        df_mostrar = df_mostrar[["nombre", "opcion_desc", "detalle"]]
        df_mostrar.rename(
            columns={
                "nombre": "Nombre",
                "opcion_desc": "Opción elegida",
                "detalle": "Detalle",
            },
            inplace=True,
        )
        st.dataframe(df_mostrar, use_container_width=True)


if __name__ == "__main__":
    main()
