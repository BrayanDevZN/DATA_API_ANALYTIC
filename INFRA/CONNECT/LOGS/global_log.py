import logging



logging.basicConfig(
        level=logging.INFO,
        filename="ADAPTER/STORAGE/LOGS/app.log",
        filemode="a",  
        encoding="utf-8",
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )