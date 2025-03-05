# ClimdexDash
Plotly-based dashboard for extreme climate indices that showcases the use of strategy design pattern for different types of data sources (e.g. csv, postgres, etc.)



or implentn netcdf fiel source (wiht post inti) that load all inot your RAM which will provide quicker access to the data (or duckdb filebased approach) in __post_init__ method of the class. This will be a better approach for the data processing part. Stay tuned for that as well or use ducddb-based approach to see how the performance is improved.
But now you will see your logic is decoupled from the whole dashboard setup therefore, more maintainable and scalable codebase. 

Notes:
- The database is not included in this repo. You can set up your own database using the scripts in this git repo.
- Loading time is still slows; you can't beat on-RAM processing. Please stay tuned for my alternative setup for the git repo.
- The csv datasource is fake.
- The dashboard only serves as
    - apply strategy design pattern for different types of data sources (e.g. csv, postgres, etc.)
    - a part of end-to-end data pipeline for climate data ingestion, processing, and visualization
- I will try to do distributed computing for the data processing part in the future. Stay tuned for that as well or use ducddb-based approach to see how the performance is improved.
- Type hints: As you can see, I play strict and loose type hints. I will try to make it more strict in the future.
