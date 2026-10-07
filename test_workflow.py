from graph.workflow import construction_workflow


# Sample project input
project_input = {
    "project_name": "Test Construction Project",
    "location": "Hyderabad",
    "plot_area": 1500,
    "builtup_area": 1200,
    "floors": 2,
    "bedrooms": 3,
    "bathrooms": 2,
    "construction_quality": "Standard",
    "material_quality": "Standard",
    "parking": "Yes",
    "budget": 2500000
}


# Run LangGraph workflow
result = construction_workflow.invoke(project_input)


print("\n========== LANGGRAPH TEST ==========")


print("\nProject Name:")
print(result.get("project_name"))


print("\nBudget:")
print(result.get("budget"))


print("\nBudget Status:")
print(result.get("budget_status"))


print("\nPredicted Construction Cost:")
print(result.get("predicted_cost"))


print("\nMaterial Estimate:")
print(result.get("material_estimate"))


print("\nTimeline:")
print(result.get("timeline"))


# --------------------------------------------------
# Budget Optimization
# --------------------------------------------------

print("\n========== BUDGET OPTIMIZATION ==========")

optimization = result.get("optimization_result")

if optimization:

    print("\nScenarios:")

    for scenario in optimization["scenarios"]:

        print("\n----------------------------------")

        print("Scenario:")
        print(scenario["Scenario"])

        print("Built-up Area:")
        print(scenario["Built-up Area"])

        print("Floors:")
        print(scenario["Floors"])

        print("Construction Quality:")
        print(scenario["Construction Quality"])

        print("Material Quality:")
        print(scenario["Material Quality"])

        print("Parking:")
        print(scenario["Parking"])

        print("Estimated Cost:")
        print(f"₹{scenario['Estimated Cost']:,.0f}")

        print("Budget Status:")
        print(scenario["Budget Status"])

        print("Budget Difference:")
        print(f"₹{scenario['Budget Difference']:,.0f}")

        print("Change Score:")
        print(scenario["Change Score"])


    print("\n========== RECOMMENDED SCENARIO ==========")

    recommended = optimization["recommended"]

    if recommended:

        print("\nRecommended Option:")
        print(recommended["Scenario"])

        print("Estimated Cost:")
        print(f"₹{recommended['Estimated Cost']:,.0f}")

        print("Budget Status:")
        print(recommended["Budget Status"])

        print("Budget Difference:")
        print(f"₹{recommended['Budget Difference']:,.0f}")

        print("Change Score:")
        print(recommended["Change Score"])

    else:

        print("\nNo generated scenario fits within the budget.")

else:

    print("\nNo optimization result available.")


# --------------------------------------------------
# Final Report
# --------------------------------------------------

print("\n========== FINAL REPORT ==========")

print("\nFinal Report:")
print(result.get("report"))


print("\n====================================")