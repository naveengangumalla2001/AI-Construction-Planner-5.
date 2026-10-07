def estimate_timeline(floors, builtup_area, construction_quality):
    """
    Estimate construction timeline in days.

    This is a preliminary planning estimate.
    It is NOT a professional construction schedule.
    """

    quality_factor = {
        "Economy": 1.00,
        "Standard": 1.10,
        "Premium": 1.20
    }

    factor = quality_factor.get(
        construction_quality,
        1.00
    )

    # -----------------------------------
    # Base construction duration
    # -----------------------------------

    site_preparation = 15

    foundation = 30

    # Structure depends mainly on number of floors
    structure = 30 * floors

    # Brick and plaster
    brick_plaster = 25 * floors

    # Electrical and plumbing
    electrical_plumbing = 15 * floors

    # Flooring and painting
    flooring_painting = 20 * floors

    # Final finishing
    finishing = 15

    # -----------------------------------
    # Apply construction quality factor
    # -----------------------------------

    site_preparation = round(
        site_preparation * factor
    )

    foundation = round(
        foundation * factor
    )

    structure = round(
        structure * factor
    )

    brick_plaster = round(
        brick_plaster * factor
    )

    electrical_plumbing = round(
        electrical_plumbing * factor
    )

    flooring_painting = round(
        flooring_painting * factor
    )

    finishing = round(
        finishing * factor
    )

    # -----------------------------------
    # Total construction duration
    # -----------------------------------

    total_days = (
        site_preparation
        + foundation
        + structure
        + brick_plaster
        + electrical_plumbing
        + flooring_painting
        + finishing
    )

    return {
        "Site Preparation": site_preparation,
        "Foundation": foundation,
        "Structure": structure,
        "Brick & Plaster": brick_plaster,
        "Electrical & Plumbing": electrical_plumbing,
        "Flooring & Painting": flooring_painting,
        "Finishing": finishing,
        "Total": total_days
    }