from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from scrapping_edital import main as scrape_edital
from scrapping_news import main as scrape_news


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_item(request: Request):
    # Call your scrapping functions
    news_data = await scrape_news()
    edital_data = await scrape_edital()

    print(news_data)  # add this line to print out the news data
    print(edital_data)  # add this line to print out the edital data

    return templates.TemplateResponse("home.html", {"request": request, "news": news_data, "editals": edital_data})