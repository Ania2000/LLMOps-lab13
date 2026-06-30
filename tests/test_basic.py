def test_simple():
    assert 2 + 2 == 4


def test_remote_data_tool_definitions():
    from src.remote_data_tools import get_tool_definitions

    tools, tool_map = get_tool_definitions()

    tool_names = [tool["function"]["name"] for tool in tools]

    assert "read_remote_csv" in tool_names
    assert "read_remote_parquet" in tool_names
    assert "read_remote_csv" in tool_map
    assert "read_remote_parquet" in tool_map


def test_dataframe_to_text():
    import polars as pl
    from src.remote_data_tools import dataframe_to_text

    df = pl.DataFrame(
        {
            "name": ["Alice", "Bob"],
            "score": [10, 20],
        }
    )

    text = dataframe_to_text(df)

    assert "Rows: 2" in text
    assert "Columns: 2" in text
    assert "name" in text
    assert "score" in text
