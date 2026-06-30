import base64
import io

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from fastmcp import FastMCP

mcp = FastMCP("Visualization server")


@mcp.tool(description="Create a line plot from one or more lists of numbers and return it as base64 PNG image.")
def line_plot(
    data: list[list[float]],
    title: str = "Line plot",
    x_label: str = "X",
    y_label: str = "Y",
    legend: bool = True,
) -> str:
    plt.figure()

    for index, series in enumerate(data):
        plt.plot(series, label=f"series_{index + 1}")

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    if legend:
        plt.legend()

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()

    buffer.seek(0)

    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    return image_base64


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        port=8003
    )
