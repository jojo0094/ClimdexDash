# **ClimdexDash**  
*A Plotly-based Dashboard for Extreme Climate Indices*  

This project demonstrates the **Strategy Design Pattern** to handle multiple data sources (CSV, PostgreSQL, etc.) for retrieving and visualizing total precipitation time series data. The implementation ensures **scalability, maintainability, and flexibility** by decoupling data retrieval logic from the dashboard setup.  

## **Overview**  
- When a user clicks on the map, the dashboard retrieves total precipitation time series data for the selected location.  
- The data retrieval is handled through strategies, currently supporting:  
  - **CSV-based source** (mock data)  
  - **PostgreSQL-based source** (real data from a weather database)  

## **Project Structure**  
- `./src/data/source.py` contains the **Strategy Pattern** implementation for handling different data sources.  
- The dashboard is built using **Dash (Plotly)** for interactive data visualization.  

---

## **Data Source Strategies**  

### **1. Utlize ABCs to define the interface for data sources**
```python
class DataSource(ABC):
    @abstractmethod
    def get_precipitation_data(self, lat: float, lon: float) -> pd.DataFrame:
        pass
```
### **2. Implement the concrete dataclasses for each data source**
```python
class CSVSource(DataSource):

    def __post_init__(self):
        """step to take care of data retieval logic from CSV file/s"""

    def get_precipitation_data(self, lat: float, lon: float) -> pd.DataFrame:
        ...
```
```python
class PostgreSQLSource(DataSource):

    def __post_init__(self):
        """step to take care of data retieval logic from PostgreSQL database"""

    def get_precipitation_data(self, lat: float, lon: float) -> pd.DataFrame:
        ...
```

### **3. Use the data source in the dashboard setup**
```python
# Initialize the data source
data_source = CSVFileSource()

# Dashboard setup code 
.......
```
or if you want to switch to PostgreSQL source, just change the data source initialization
```python
# Initialize the data source
data_source = PostgreDataSource()

# Dashboard setup code
.......
```
Like above, once the data retrieval logic is decoupled from the dashboard setup, it becomes easier to add more data sources without modifying the existing codebase. For example, adding a NetCDF source would require creating a new dataclass that implements the `DataSource` interface.

You can just create the following code to implement the NetCDF source without modifying the existing dashboard setup thanks to the decoupled benefits offered by the Strategy Pattern.
```python
class NetCDFSource(DataSource):

    def __post_init__(self):
        """step to take care of data retieval logic from NetCDF file/s"""

    def get_precipitation_data(self, lat: float, lon: float) -> pd.DataFrame:
        ...
```

### **5. Currently, only PostgresDataSource is implemented while others were just mocked for demonstration purposes.**

### **6. Other consideration
- **NetCDF Source**: Loads the dataset into RAM at initialization (`__post_init__`) to provide **faster analytical access**.  
- **DuckDB Source**: A **file-based approach** for improved performance over traditional databases.  
- **Distributed Computing**: Exploring parallelization for large-scale climate data processing through BigQuery, Spark, etc.

---

## **Key Features**  
✅ **Strategy Design Pattern**: Allows seamless switching between different data sources.  
✅ **Decoupled Logic**: Enhances maintainability and reusability of the codebase.  
✅ **Extensible Framework**: Easily add more data sources without modifying existing logic.  
✅ **Interactive Visualization**: Dash + Plotly integration for extreme climate indices exploration.  

---

## **Notes**  
🚀 The database is **not included** in this repository. You can set up your own using the provided SQL scripts in  
[ReanalysisIngestion Repository](https://github.com/jojo0094/ReanalysisIngestion)  

🖥️ This project runs on a **low-capacity remote compute unit**, so the dataset is currently limited to **1-5 years**.  
⏳ Loading time is still slow, but **on-RAM processing (NetCDF/DuckDB)** should significantly improve performance.  
🔧 **Type hints**: I plan to refine this further.  

---

## **Future Plans**  
- ✅ Implement **NetCDF and DuckDB data sources** for enhanced performance.  
- ✅ Improve **distributed computing** capabilities for large-scale climate data processing.  
- ✅ Refine **type hinting and optimizations** for better readability and robustness.  

Stay tuned for upcoming updates! 🚀  

