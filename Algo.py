def calculate_affordability(df, annual_income, bedrooms):
    # Convert annual income to monthly
    monthly_income = annual_income / 12
    
    # 30% rule
    affordable_rent = monthly_income * 0.3
    
    # Select correct FMR column
    rent_col = f"fmr_{bedrooms}"
    
    # Avoid modifying original dataframe
    df = df.copy()
    
    # Calculate affordability ratio
    df["affordability_ratio"] = df[rent_col] / affordable_rent
    
    # Create affordability score (higher = better)
    df["affordability_score"] = 100 - (df["affordability_ratio"] * 100)
    
    # Clip scores between 0 and 100
    df["affordability_score"] = df["affordability_score"].clip(lower=0, upper=100)
    
    # Label categories
    def label(row):
        if row["affordability_ratio"] <= 1:
            return "Affordable"
        elif row["affordability_ratio"] <= 1.2:
            return "Moderately Affordable"
        else:
            return "Not Affordable"
    
    df["affordability_label"] = df.apply(label, axis=1)
    
    # Sort best options
    df = df.sort_values(by="affordability_score", ascending=False)
    
    return df