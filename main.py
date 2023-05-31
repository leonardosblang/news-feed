from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from scrapping_edital import main as scrape_edital
from scrapping_news import main as scrape_news


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_item(request: Request):

    news_data = await scrape_news()
    edital_data = await scrape_edital()

    print(news_data)
    print(edital_data)

    return templates.TemplateResponse("home.html", {"request": request, "news": news_data, "editals": edital_data})