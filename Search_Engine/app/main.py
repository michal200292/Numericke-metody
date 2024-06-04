from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from process_query import search_query

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse, status_code=201)
async def get_basic_form(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get('/query/', response_class=HTMLResponse, status_code=201)
async def get_basic_form(request: Request, query: str):
    results = search_query(query)
    return templates.TemplateResponse(
        request=request,
        name="search_results.html",
        context={"results": results}
    )
