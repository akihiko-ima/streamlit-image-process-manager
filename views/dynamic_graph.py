import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time


def show():
    st.subheader("Sin波アニメーション", divider="gray")

    if "run" not in st.session_state:
        st.session_state.run = False

    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "Start",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.run = True
    with col2:
        if st.button(
            "Stop",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.run = False

    def run_animation():
        frequency, amplitude, speed, window_size, initial_phase = 1, 1, 0.1, 100, 0
        x = np.linspace(0, 4 * np.pi, window_size)
        placeholder = st.empty()
        fig, ax = plt.subplots()
        (line,) = ax.plot([], [], color="blue")
        ax.set_ylim(-1.5, 1.5)
        ax.set_xlim(0, 20)
        ax.set_title("Sin animation")
        for t in range(1000):
            if not st.session_state.run:
                break
            phase = initial_phase + t * speed
            y = amplitude * np.sin(frequency * x + phase)
            line.set_data(x, y)
            fig.canvas.draw()
            image = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
            image = image.reshape(fig.canvas.get_width_height()[::-1] + (4,))
            placeholder.image(image, use_container_width=True)
            time.sleep(0.05)
        st.toast("アニメーション終了")

    if st.session_state.run:
        run_animation()
