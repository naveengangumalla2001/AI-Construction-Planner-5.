import pandas as pd


def optimize_budget(
    budget,
    predicted_cost,
    construction_quality,
    material_quality,
    builtup_area,
    floors,
    parking
):
    """
    Preliminary rule-based budget optimization.

    This module provides planning suggestions only.
    Final construction decisions must be validated
    by qualified construction professionals.
    """

    suggestions = []

    # ---------------------------------------------------------
    # CHECK WHETHER PROJECT IS WITHIN BUDGET
    # ---------------------------------------------------------

    if predicted_cost <= budget:

        return {
            "status": "Within Budget",
            "budget": budget,
            "current_cost": predicted_cost,
            "savings_required": 0,
            "suggestions": [
                "Current project estimate is within the planned budget."
            ]
        }

    # Amount that needs to be reduced
    savings_required = predicted_cost - budget

    # ---------------------------------------------------------
    # CONSTRUCTION QUALITY OPTIMIZATION
    # ---------------------------------------------------------

    if construction_quality == "Premium":

        suggestions.append({
            "change": "Premium → Standard Construction Quality",
            "reason": "Reduce construction quality level",
            "impact": "Potential cost reduction"
        })

    # ---------------------------------------------------------
    # MATERIAL QUALITY OPTIMIZATION
    # ---------------------------------------------------------

    if material_quality == "Premium":

        suggestions.append({
            "change": "Premium → Standard Material Quality",
            "reason": "Use standard-grade materials",
            "impact": "Potential material cost reduction"
        })

    # ---------------------------------------------------------
    # BUILT-UP AREA OPTIMIZATION
    # ---------------------------------------------------------

    if builtup_area > 1500:

        suggestions.append({
            "change": "Reduce Built-up Area",
            "reason": (
                "Lower built-up area can reduce "
                "material and labour requirements"
            ),
            "impact": "Potential significant cost reduction"
        })

    # ---------------------------------------------------------
    # FLOOR OPTIMIZATION
    # ---------------------------------------------------------

    if floors > 1:

        suggestions.append({
            "change": "Review Number of Floors",
            "reason": (
                "Reducing floors can reduce structural "
                "and finishing costs"
            ),
            "impact": "Potential cost reduction"
        })

    # ---------------------------------------------------------
    # PARKING OPTIMIZATION
    # ---------------------------------------------------------

    if parking == "Yes":

        suggestions.append({
            "change": "Review Parking Requirement",
            "reason": (
                "Consider whether dedicated parking "
                "construction is necessary"
            ),
            "impact": "Potential cost reduction"
        })

    return {
        "status": "Over Budget",
        "budget": budget,
        "current_cost": predicted_cost,
        "savings_required": savings_required,
        "suggestions": suggestions
    }


# =============================================================
# ML-BASED SCENARIO GENERATION
# =============================================================

def generate_scenarios(
    model,
    budget,
    plot_area,
    builtup_area,
    floors,
    bedrooms,
    bathrooms,
    location,
    construction_quality,
    material_quality,
    parking
):
    """
    Generate alternative construction scenarios.

    Each scenario is passed to the trained ML cost prediction
    model to estimate the construction cost.

    These are preliminary planning scenarios and are not
    architectural or structural recommendations.
    """

    scenarios = []

    # ---------------------------------------------------------
    # 1. CURRENT PLAN
    # ---------------------------------------------------------

    scenarios.append({
        "Scenario": "Current Plan",
        "Built-up Area": builtup_area,
        "Floors": floors,
        "Construction Quality": construction_quality,
        "Material Quality": material_quality,
        "Parking": parking
    })

    # ---------------------------------------------------------
    # 2. STANDARD CONSTRUCTION
    # ---------------------------------------------------------

    if construction_quality == "Premium":

        scenarios.append({
            "Scenario": "Standard Construction",
            "Built-up Area": builtup_area,
            "Floors": floors,
            "Construction Quality": "Standard",
            "Material Quality": material_quality,
            "Parking": parking
        })

    # ---------------------------------------------------------
    # 3. STANDARD MATERIALS
    # ---------------------------------------------------------

    if material_quality == "Premium":

        scenarios.append({
            "Scenario": "Standard Materials",
            "Built-up Area": builtup_area,
            "Floors": floors,
            "Construction Quality": construction_quality,
            "Material Quality": "Standard",
            "Parking": parking
        })

    # ---------------------------------------------------------
    # 4. STANDARD CONSTRUCTION + MATERIALS
    # ---------------------------------------------------------

    if (
        construction_quality == "Premium"
        and material_quality == "Premium"
    ):

        scenarios.append({
            "Scenario": "Standard Construction + Materials",
            "Built-up Area": builtup_area,
            "Floors": floors,
            "Construction Quality": "Standard",
            "Material Quality": "Standard",
            "Parking": parking
        })

    # ---------------------------------------------------------
    # 5. REDUCED BUILT-UP AREA
    # ---------------------------------------------------------

    if builtup_area > 1000:

        reduced_area = round(builtup_area * 0.90)

        scenarios.append({
            "Scenario": "Reduced Built-up Area",
            "Built-up Area": reduced_area,
            "Floors": floors,
            "Construction Quality": construction_quality,
            "Material Quality": material_quality,
            "Parking": parking
        })

    # ---------------------------------------------------------
    # 6. REDUCED FLOORS
    # ---------------------------------------------------------

    if floors > 1:

        scenarios.append({
            "Scenario": "Reduced Floors",
            "Built-up Area": builtup_area,
            "Floors": floors - 1,
            "Construction Quality": construction_quality,
            "Material Quality": material_quality,
            "Parking": parking
        })

    # =========================================================
    # PREDICT COST FOR EACH SCENARIO
    # =========================================================

    results = []

    for scenario in scenarios:

        input_data = {
            "plot_area_sqft": plot_area,
            "builtup_area_sqft": scenario["Built-up Area"],
            "floors": scenario["Floors"],
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "location": location,
            "construction_quality": scenario["Construction Quality"],
            "material_quality": scenario["Material Quality"],
            "parking": scenario["Parking"]
        }

        # Convert input into DataFrame
        input_df = pd.DataFrame([input_data])

        # ML model prediction
        predicted_cost = float(
            model.predict(input_df)[0]
        )

        # Copy scenario information
        result = scenario.copy()

        # -----------------------------------------------------
        # ESTIMATED COST
        # -----------------------------------------------------

        result["Estimated Cost"] = round(
            predicted_cost
        )

        # -----------------------------------------------------
        # BUDGET STATUS
        # -----------------------------------------------------

        result["Budget Status"] = (
            "Within Budget"
            if predicted_cost <= budget
            else "Over Budget"
        )

        # -----------------------------------------------------
        # BUDGET DIFFERENCE
        # -----------------------------------------------------

        result["Budget Difference"] = round(
            budget - predicted_cost
        )

        # -----------------------------------------------------
        # CHANGE SCORE
        # -----------------------------------------------------
        #
        # Lower score = fewer changes from the client's
        # original requirements.
        #
        # Built-up area change  → 3 points
        # Floor change          → 3 points
        # Construction quality → 2 points
        # Material quality      → 2 points
        # Parking change        → 1 point
        #
        # This helps the recommendation prefer solutions
        # that preserve the client's original requirements.

        change_score = 0

        if scenario["Built-up Area"] != builtup_area:
            change_score += 3

        if scenario["Floors"] != floors:
            change_score += 3

        if (
            scenario["Construction Quality"]
            != construction_quality
        ):
            change_score += 2

        if (
            scenario["Material Quality"]
            != material_quality
        ):
            change_score += 2

        if scenario["Parking"] != parking:
            change_score += 1

        result["Change Score"] = change_score

        # Add result
        results.append(result)

    return results