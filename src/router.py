import streamlit as st
from streamlit_option_menu import option_menu

from views import (
    main_manage,
    only_streamlit_function,
    processed_check_page,
    comment_page,
    README,
    dynamic_graph,
)


def router():
    # Bootstrap Icons
    # https://icons.getbootstrap.com/
    with st.sidebar:
        selected = option_menu(
            "IPM",
            ["Home", "Upload", "Manage", "Comment", "README", "graph"],
            icons=[
                "house",
                "bi-upload",
                "database",
                "gear",
                "bi-bell",
                "bi-graph-up-arrow",
            ],
            menu_icon="bi-camera",
            default_index=0,
        )

    if selected == "Home":
        main_manage.show()
    elif selected == "Upload":
        only_streamlit_function.show()
    elif selected == "Manage":
        processed_check_page.show()
    elif selected == "Comment":
        comment_page.show()
    elif selected == "README":
        README.show()
    elif selected == "graph":
        dynamic_graph.show()
