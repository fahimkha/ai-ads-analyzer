def generate_recommendations(row):
    recs = []

    # CTR rules
    if row.get("ctr", 0) < 1:
        recs.append("Improve ad creative or headline (Low CTR)")

    # CPC rules
    if row.get("cpc", 0) > 1.5:
        recs.append("Test new audience targeting (High CPC)")

    # Conversions
    if row.get("conversions", 0) < 5:
        recs.append("Improve landing page or offer")

    # CPA
    if row.get("cpa", 0) > 50:
        recs.append("Pause or reduce budget (High CPA)")

    # ROAS
    if row.get("roas", 0) > 3:
        recs.append("Scale this ad (Increase budget 20-30%)")

    # Impressions / Clicks suggestions
    if row.get("clicks", 0) < 5 and row.get("impressions", 0) > 100:
        recs.append("Ad has low engagement; test different creatives")

    return " | ".join(recs)
