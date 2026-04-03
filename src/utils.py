def map_cluster_to_segment(df):

    cluster_summary = df.groupby("cluster")["clv"].mean().sort_values()

    labels = [
        "Low Value Customers",
        "At Risk Customers",
        "Loyal Customers",
        "High Value Customers"
    ]

    mapping = {
        cluster: labels[i]
        for i, cluster in enumerate(cluster_summary.index)
    }

    df["segment"] = df["cluster"].map(mapping)

    return df