# dan data engineering 2

A project of mine to scrap board game prices and availability and visualize the history

Graph:

![](./diagram.drawio.svg)

![](./image.png)

## get started

`python daily_scrap_workflow.py`

## prod

`python create_deployment.py`

`DATABASE_URL = "postgresql+psycopg2://user:password@host/db_name"` needs to be set in a block in prefect
