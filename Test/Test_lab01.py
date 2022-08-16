import asyncio
from ymProject.API import jx3_Daily as Daily

daily = Daily.GetDaily()
asyncio.run(daily.QueryDailyFigure())
