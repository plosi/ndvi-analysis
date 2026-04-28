import ee
import geemap
import pandas as pd

def extract_timeseries_to_region(
    image_collection:ee.ImageCollection,
    aoi:ee.Geometry | ee.Feature | ee.FeatureCollection,
    bands:list,
    scale:int,
    start_date:str | None = None,
    end_date:str | None = None,
    reducer:ee.Reducer = ee.Reducer.median()
) -> pd.DataFrame:
    """
    Extracts a time series of reduced values from an ImageCollection over a specified area of interest and time range.

    Args:
        image_collection (ee.ImageCollection): The ImageCollection to extract data from.
        aoi (ee.Geometry): The area of interest to reduce over.
        start_date (str): The start date for filtering the ImageCollection (format: 'YYYY-MM-DD').
        end_date (str): The end date for filtering the ImageCollection (format: 'YYYY-MM-DD').
        bands (list): A list of band names to extract from each image.
        scale (int): The scale at which to perform the reduction.
        reducer (ee.Reducer, optional): The reducer to apply to the images. Defaults to ee.Reducer.median().
    
    Returns:
        pd.DataFrame: A DataFrame containing the date and reduced values for each specified band.
    
        
    Notes:
        - Reduction is performed server-side using reduceRegion().
        - Missing or fully masked values will appear as NaN in the output.
        - One client-server request is made per band.

    """
    if not isinstance(bands, (list, tuple)) or len(bands) == 0:
        raise ValueError("bands must be a non-empty list of band names")
    
    if scale <= 0:
        raise ValueError("scale must be a positive integer")
    
    
    # Normalize AOI
    if isinstance(aoi, ee.Feature):
        aoi = aoi.geometry()
    elif isinstance(aoi, ee.FeatureCollection):
        aoi = aoi.geometry()


    # Filter the ImageCollection by date and bounds
    filtered_ic = (
        image_collection
        .select(bands)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.bounds(aoi))
    )
    
    # Function to reduce each image to a feature with the date and reduced values
    def _img_to_feature(img):
        stats = img.reduceRegion(
            reducer = reducer,
            geometry = aoi,
            scale = scale,
            maxPixels = 1e9
        )
        values = {band: stats.get(band) for band in bands}

        return ee.Feature(
            None,
            {
                "date": img.date().format("YYYY-MM-dd"),
                **values
            }
        )
    
    # Map the function over the filtered ImageCollection
    ts_features = filtered_ic.map(_img_to_feature)
    # Extract the date and reduced values into lists
    dates = ts_features.aggregate_array("date").getInfo()
    data = {band: ts_features.aggregate_array(band).getInfo() for band in bands}
    # Create a DataFrame from the extracted data
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(dates),
            **data
        }
    )

    return df.sort_values("date")