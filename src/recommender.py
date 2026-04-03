def get_strategy(segment):
    return {
        "High Value Customers": "Upsell premium products, exclusive deals",
        "Loyal Customers": "Loyalty rewards & memberships",
        "At Risk Customers": "Reactivation campaigns & discounts",
        "Low Value Customers": "Engagement campaigns & offers"
    }.get(segment, "No strategy found")