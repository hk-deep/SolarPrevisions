# ----------------------------------------------------------------------------------------------------------
# Fonctions pour charger proprement les fichiers csv sur python (!!! testé pour python version >= 3.12 !!!)
# ----------------------------------------------------------------------------------------------------------

from pathlib import Path
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------------------------------------

def _concat_datasets_from_dict(
    dataset_dict: dict[xr.Dataset | xr.DataArray],
    new_dim_name: str,
) -> xr.Dataset | xr.DataArray:
    """Concatenate a dict of dataset along a new dimension with keys as coordinates."""
    # Check if the dictionary is not empty
    if not dataset_dict:
        msg = "The dictionary of datasets is empty."
        raise ValueError(msg)
    # Align the datasets on common coordinates (if needed)
    datasets = xr.align(*list(dataset_dict.values()))
    # Concatenate the datasets along the new dimension, using the keys as coordinates
    return xr.concat(
        datasets,
        dim=new_dim_name,
        combine_attrs="override",
    ).assign_coords({new_dim_name: list(dataset_dict.keys())})

# -----------------------------------------------------------------

def load_e4cast_result_sheet(
    filepath: str | Path,
) -> xr.DataArray:
    """Load e4cast3.0 simulation result file."""
    try:
        results = pd.read_csv(
            filepath,
            index_col="initial_timeslot",
            parse_dates=["initial_timeslot"],
            date_format="ISO8601",
            header=0,
            na_values=[""],
            dtype=float,
        )

    except FileNotFoundError as filenotfound:
        msg = (
            f'Result file: "{filepath}" not found. '
            'Running at least one "process" is required before post-processing.'
        )
        filenotfound.add_note(msg)
        raise

    # Decode and parse ISO08601 timedeltas and datetimes
    results.index = pd.to_datetime(results.index).tz_convert(None)

    # Remove potential duplicates
    results_ds = xr.Dataset.from_dataframe(
        results[~results.index.duplicated(keep="first")].sort_values(
            by="initial_timeslot"
        ),
    )

    horizons = list(results_ds.data_vars)
    da_dict = {horizon: results_ds[horizon] for horizon in horizons}
    return (
        _concat_datasets_from_dict(dataset_dict=da_dict, new_dim_name="horizon")
        .rename("var")
        .astype(float)
    )

# -----------------------------------------------------------------

if __name__ == "__main__":
    # Base dir
    base_dir = Path("/home/vduchemin/backtest_fine4cast/TP_polytechnique_data/")
    # Files
    file_ghi_fcst_e4cast = base_dir.joinpath("ghi_sirta_e4cast3_forecast_results.csv")
    file_ghi_fcst_arome = base_dir.joinpath("ghi_arome.csv")
    file_ghi_sirta = base_dir.joinpath("ghi_measurements_sirta.csv")
    # Data
    ghi = load_e4cast_result_sheet(file_ghi_fcst_e4cast).rename("ghi_e4c").to_dataset()
    ghi["ghi_arome"] = load_e4cast_result_sheet(file_ghi_fcst_arome)
    ghi["ghi_sirta"] = load_e4cast_result_sheet(file_ghi_sirta)
    # Display e4cast forecast
    print("-------- GHI DATASET --------")
    print(ghi)
    print("-----------------------------")
    print("----- GHI E4C DATAARRAY -----")
    print(ghi["ghi_e4c"])
    print("-----------------------------")
    # Parsing
    timestamp = pd.Timestamp(year=2023, month=6, day=14, hour=11, minute=11)
    fig = plt.figure()
    ghi["ghi_sirta"].sel(initial_timeslot=timestamp, method="nearest").plot(label="GHI Mesuré (SIRTA)")
    ghi["ghi_arome"].sel(initial_timeslot=timestamp, method="nearest").plot(label="GHI Prévu (AROME)")
    ghi["ghi_e4c"].sel(initial_timeslot=timestamp, method="nearest").plot(label="GHI Prévu (E4cast)")
    # Titles
    plt.title(f"Prévisions GHI pour le {timestamp.strftime('%d-%m-%Y %H:%M')}", weight="bold")
    plt.xlabel("Heure", weight="bold")
    plt.ylabel("GHI (W/m²)", weight="bold")
    # Axes
    x_start = ghi.coords["horizon"].to_numpy()[0]
    x_end = ghi.coords["horizon"].to_numpy()[-1]
    plt.xlim(left=x_start, right=x_end)
    # Modify x ticks
    ax = plt.gca()
    horizons = ax.get_xticks()
    new_labels = [
        (timestamp + pd.Timedelta(str(horizon))).strftime("%H:%M")
        for horizon in ghi.coords["horizon"].to_numpy()
    ]
    plt.xticks(ticks=horizons, labels=new_labels, rotation=45, ha='right', rotation_mode='anchor')
    # Building image
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.show()
