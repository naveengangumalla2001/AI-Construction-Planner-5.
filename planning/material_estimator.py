def estimate_materials(builtup_area, construction_quality):

    # Indicative construction coefficients
    # These are preliminary planning assumptions,
    # not structural/engineering specifications.

    quality_factor = {
        "Economy": 0.90,
        "Standard": 1.00,
        "Premium": 1.10
    }

    factor = quality_factor.get(construction_quality, 1.00)

    # Material estimation
    cement_bags = builtup_area * 0.40 * factor
    steel_kg = builtup_area * 4.0 * factor
    sand_cuft = builtup_area * 1.80 * factor
    aggregate_cuft = builtup_area * 1.30 * factor
    bricks = builtup_area * 8 * factor

    return {
        "Cement (bags)": round(cement_bags),
        "Steel (kg)": round(steel_kg),
        "Sand (m³)": round(sand_cuft * 0.0283168, 2),
        "Aggregate (m³)": round(aggregate_cuft * 0.0283168, 2),
        "Bricks (approx.)": round(bricks)
    }