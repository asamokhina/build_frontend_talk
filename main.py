import io
import os
from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd
from fastapi import FastAPI, Response, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse, StreamingResponse

from data import create_basic_plot, get_data

location = os.path.dirname(os.path.realpath(__file__))
frontend = os.path.join(location, "client", "build")
templates = Jinja2Templates(directory="templates")

app = FastAPI()

# add frontend build files to the app,
# without mounting FastAPI can't see all the required files
app.mount("/", StaticFiles(directory=frontend, html=True))

# basic steps data
@app.get("/view/basic-steps")
def read_basicsteps() -> Dict[str, Dict[str, int]]:
    df: pd.DataFrame = get_data()
    return df.to_dict(orient="index")


# steps data as HTML table with pandas
@app.get("/view/pandas-steps")
def read_pandassteps():
    df = get_data()
    return HTMLResponse(df.to_html())


# steps data as a custom HTML table
@app.get("/view/basic-html-steps")
def read_basic_html_steps(response: Response) -> str:
    df = get_data()
    max_idx = df["Actual"].idxmax()

    table_start = "<table style='border-collapse: collapse;'>"
    end_table = "</table>"

    start_head = "<thead style='background-color: #F5F5F5;'>"
    end_head = "</thead>"

    start_row = "<tr>"
    end_row = "</tr>"

    date_column_style = "<th style='padding: 8px; border: 1px solid #ddd;'>Date</th>"
    steps_column_style = "<th style='padding: 8px; border: 1px solid #ddd;'>Steps</th>"
    start_body = "<tbody>"
    end_body = "</tbody>"

    html_table = (
        table_start
        + start_head
        + start_row
        + date_column_style
        + steps_column_style
        + end_row
        + end_head
        + start_body
    )

    for index, row in df.iterrows():
        bg_color = "background-color: #3b7a57;" if index == max_idx else ""

        html_table += (
            f"<tr style='{bg_color} border: 1px solid #ddd;'><td style='padding: 8px; border: 1px solid #ddd;'>"
            + str(index)
            + f"</td><td style='padding: 8px; border: 1px solid #ddd;'>"
            + str(row["Actual"])
            + "</td></tr>"
        )
    html_table += end_body + end_table
    return HTMLResponse(html_table)


@app.get(
        "/view/template-table",
        response_class=HTMLResponse
)
async def template_table(request: Request):
    df = get_data()
    idx_max = df["Actual"].idxmax()

    return templates.TemplateResponse(
        name="table.html",
        context={
            "request": request,
            "df": df,
            "idx_max": idx_max,
        },
    )


# matplotlib plot of steps data
@app.get("/view/matplotlib-plot")
def read_matplotlib_plot():
    df = get_data()
    create_basic_plot(df)

    buffer = io.BytesIO()
    # calls `gcf()` function to get the current figure from the pyplot figure stack
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    return Response(content=buffer.getvalue(), media_type="image/png")


@app.get("/svelte-steps")
def js_frontend():
    return FileResponse(os.path.join(frontend, "steps.html"))


# utils endpoint to check all urls
@app.get("/content")
def content():
    urls = "</br>".join(
        f"<a href={route.path}>{route.name}</a>" for route in app.routes
    )

    return HTMLResponse(urls)

