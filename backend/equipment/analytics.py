import pandas as pd


def analyze_csv(file_path):
    """
    Reads CSV and returns summary analytics.

    ✅ Supports:
    - Web React Dashboard (Table + Charts)
    - Desktop PyQt Dashboard (Table + Charts)
    - PDF Report Generation
    """

    df = pd.read_csv(file_path)

    # ✅ Required Columns Validation (Screening Task Columns)
    required_cols = ["Type", "Flowrate", "Pressure", "Temperature"]

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # ✅ Clean numeric columns safely
    df["Flowrate"] = pd.to_numeric(df["Flowrate"], errors="coerce")
    df["Pressure"] = pd.to_numeric(df["Pressure"], errors="coerce")
    df["Temperature"] = pd.to_numeric(df["Temperature"], errors="coerce")

    # ✅ Remove invalid rows
    df = df.dropna(subset=["Flowrate", "Pressure", "Temperature"])

    # ✅ Preview Limit (Task requires table display)
    preview_rows = df.head(10)

    # ✅ Summary Response (API Contract)
    summary = {
        # -------------------------------
        # ✅ Core Statistics
        # -------------------------------
        "total_count": int(len(df)),
        "avg_flowrate": round(df["Flowrate"].mean(), 2),
        "avg_pressure": round(df["Pressure"].mean(), 2),
        "avg_temperature": round(df["Temperature"].mean(), 2),

        # -------------------------------
        # ✅ Distribution
        # -------------------------------
        "type_distribution": df["Type"].value_counts().to_dict(),

        # -------------------------------
        # ✅ Data Lists (for charts if needed)
        # -------------------------------
        "flowrate_list": df["Flowrate"].tolist(),
        "pressure_list": df["Pressure"].tolist(),
        "temperature_list": df["Temperature"].tolist(),

        # -------------------------------
        # ✅ Data Table Preview (Frontend Requirement)
        # -------------------------------
        "preview_columns": list(preview_rows.columns),
        "data_preview": preview_rows.to_dict(orient="records"),
    }

    return summary