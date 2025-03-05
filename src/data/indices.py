import xclim
from dataclasses import dataclass
import pandas as pd
import xarray as xr

@dataclass
class ClimateIndices:
    data : pd.DataFrame

    def __post_init__(self):
        pr = xr.DataArray(self.data['total_precipitation'], dims=['time'], coords={'time': self.data['time']}, attrs={'units': 'mm'})
        pr = xclim.units.amount2rate(pr)
        self.dataarray = pr 

    def maximum_consecutive_wet_days(self, freq: str = "YS") -> xr.DataArray:
        """Maximum number of consecutive wet days."""
        return xclim.indices.maximum_consecutive_wet_days(self.dataarray, freq=freq)

    def maximum_consecutive_dry_days(self, freq: str = "YS") -> xr.DataArray:
        """Maximum number of consecutive dry days."""
        return xclim.indices.maximum_consecutive_dry_days(self.dataarray, freq=freq)

    def max_n_day_precipitation_amount(self, n: int, freq: str = "YS") -> xr.DataArray:
        """Maximum n-day precipitation amount."""
        return xclim.indices.max_n_day_precipitation_amount(self.dataarray, window=n, freq=freq)
