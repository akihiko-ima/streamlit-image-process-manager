import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode


def configure_aggrid(data: pd.DataFrame) -> pd.DataFrame:
    """
    AgGridの設定を行い、選択されたデータを返す関数。

    Args:
        data (pd.DataFrame): 表示するデータフレーム。

    Returns:
        pd.DataFrame: ユーザーが選択した行のデータフレーム。
    """
    grid_builder = GridOptionsBuilder.from_dataframe(
        data,
        editable=False,
        filter=True,
        resizable=True,
        sortable=True,
    )
    grid_builder.configure_selection(selection_mode="multiple", use_checkbox=True)
    grid_builder.configure_side_bar(filters_panel=True, columns_panel=False)
    grid_builder.configure_default_column(
        enablePivot=True, enableValue=True, enableRowGroup=True
    )
    grid_builder.configure_grid_options(rowHeight=50)

    grid_options = grid_builder.build()
    grid_options["columnDefs"][0]["checkboxSelection"] = True

    with st.container():
        response = AgGrid(
            data,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.MODEL_CHANGED,
            theme="alpine",
        )

    return pd.DataFrame(response["selected_rows"])
