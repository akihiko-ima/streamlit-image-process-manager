import pandas as pd


def format_datetime_column(df, column_name, format_str="%Y/%m/%d %H:%M"):
    """
    指定されたDataFrameの列を指定された日付形式にフォーマットします。

    Args:
        df (pd.DataFrame): 対象のDataFrame。
        column_name (str): フォーマットする列名。
        format_str (str): 日付フォーマットの文字列（デフォルト: "%Y/%m/%d %H:%M"）。

    Returns:
        pd.DataFrame: フォーマット後のDataFrame。
    """
    if column_name in df.columns:
        df[column_name] = pd.to_datetime(df[column_name]).dt.strftime(format_str)
    return df
