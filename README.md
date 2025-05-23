Primary user function:
  wire_read(filename, as_numpy=False, as_pandas=False, map_data=False, verbose=False)

If no format (numpy or pandas) are specified, contents are returned as lists.

As numpy, contents are returned as a (n,2) array of X values, intensities.

As pandas, contents are returned as a DataFrame with labels 'XLST' and 'DATA' for X values and intensities.

Map data is supported in the backend, but not currently accessible via the frontend.
