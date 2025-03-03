from prefect import flow
from games import games

# Source for the code to deploy (here, a GitHub repo)
SOURCE_REPO = "https://github.com/cubbK/gmt_availability_scrap_prefect.git"

if __name__ == "__main__":
    flow.from_source(
        source=SOURCE_REPO,
        entrypoint="./daily_scrap_workflow.py:track_availability",
    ).deploy(
        name="daily_scrap_workflow",
        parameters={"games": games},
        work_pool_name="gmt_availability_scrap_work_pool",
        cron="0 0 * * *",  # Run daily
    )
