import math
import plotly.graph_objects as go


def create_floor_plan(
    plot_area,
    builtup_area,
    bedrooms,
    bathrooms,
    parking="No"
):
    """
    Create a conceptual 2D floor plan.

    This is a preliminary visualization for planning purposes.
    It is NOT an architectural or structural drawing.
    """

    # --------------------------------------------------
    # 1. Calculate approximate plot dimensions
    # --------------------------------------------------

    plot_side = math.sqrt(plot_area)

    # Keep a reasonable rectangular proportion
    plot_width = plot_side
    plot_length = plot_area / plot_width

    # --------------------------------------------------
    # 2. Calculate approximate built-up dimensions
    # --------------------------------------------------

    builtup_side = math.sqrt(builtup_area)

    building_width = builtup_side
    building_length = builtup_area / building_width

    # --------------------------------------------------
    # 3. Create figure
    # --------------------------------------------------

    fig = go.Figure()

    # --------------------------------------------------
    # 4. Plot boundary
    # --------------------------------------------------

    fig.add_shape(
        type="rect",
        x0=0,
        y0=0,
        x1=plot_width,
        y1=plot_length,
        line=dict(width=3),
    )

    # --------------------------------------------------
    # 5. Building boundary
    # --------------------------------------------------

    building_x0 = (plot_width - building_width) / 2
    building_y0 = (plot_length - building_length) / 2

    building_x1 = building_x0 + building_width
    building_y1 = building_y0 + building_length

    fig.add_shape(
        type="rect",
        x0=building_x0,
        y0=building_y0,
        x1=building_x1,
        y1=building_y1,
        line=dict(width=3),
    )

    # --------------------------------------------------
    # 6. Generate approximate rooms
    # --------------------------------------------------

    rooms = []

    # Number of bedrooms
    bedroom_count = max(1, int(bedrooms))

    # Divide building into approximate room sections
    room_width = building_width / 2
    room_height = building_length / 3

    # Bedrooms
    for i in range(bedroom_count):

        row = i // 2
        col = i % 2

        x0 = building_x0 + col * room_width
        y0 = building_y0 + row * room_height

        x1 = x0 + room_width
        y1 = y0 + room_height

        rooms.append(
            {
                "name": f"Bedroom {i + 1}",
                "x0": x0,
                "y0": y0,
                "x1": x1,
                "y1": y1,
            }
        )

    # --------------------------------------------------
    # 7. Bathroom area
    # --------------------------------------------------

    bathroom_count = max(1, int(bathrooms))

    bathroom_width = building_width / 4
    bathroom_height = building_length / 5

    for i in range(bathroom_count):

        x0 = building_x1 - bathroom_width
        y0 = building_y0 + i * bathroom_height

        x1 = building_x1
        y1 = y0 + bathroom_height

        rooms.append(
            {
                "name": f"Bathroom {i + 1}",
                "x0": x0,
                "y0": y0,
                "x1": x1,
                "y1": y1,
            }
        )

    # --------------------------------------------------
    # 8. Add room shapes
    # --------------------------------------------------

    for room in rooms:

        fig.add_shape(
            type="rect",
            x0=room["x0"],
            y0=room["y0"],
            x1=room["x1"],
            y1=room["y1"],
            line=dict(width=1),
        )

        center_x = (room["x0"] + room["x1"]) / 2
        center_y = (room["y0"] + room["y1"]) / 2

        fig.add_annotation(
            x=center_x,
            y=center_y,
            text=room["name"],
            showarrow=False,
        )

    # --------------------------------------------------
    # 9. Living Room
    # --------------------------------------------------

    living_x0 = building_x0
    living_y0 = building_y0 + building_length * 0.65

    living_x1 = building_x0 + building_width * 0.60
    living_y1 = building_y1

    fig.add_shape(
        type="rect",
        x0=living_x0,
        y0=living_y0,
        x1=living_x1,
        y1=living_y1,
        line=dict(width=1),
    )

    fig.add_annotation(
        x=(living_x0 + living_x1) / 2,
        y=(living_y0 + living_y1) / 2,
        text="Living Room",
        showarrow=False,
    )

    # --------------------------------------------------
    # 10. Kitchen
    # --------------------------------------------------

    kitchen_x0 = building_x0 + building_width * 0.60
    kitchen_y0 = building_y0 + building_length * 0.65

    kitchen_x1 = building_x1
    kitchen_y1 = building_y1

    fig.add_shape(
        type="rect",
        x0=kitchen_x0,
        y0=kitchen_y0,
        x1=kitchen_x1,
        y1=kitchen_y1,
        line=dict(width=1),
    )

    fig.add_annotation(
        x=(kitchen_x0 + kitchen_x1) / 2,
        y=(kitchen_y0 + kitchen_y1) / 2,
        text="Kitchen",
        showarrow=False,
    )

    # --------------------------------------------------
    # 11. Parking
    # --------------------------------------------------

    if parking == "Yes":

        parking_width = min(plot_width * 0.35, 20)
        parking_height = min(plot_length * 0.20, 15)

        parking_x0 = 0
        parking_y0 = 0

        parking_x1 = parking_x0 + parking_width
        parking_y1 = parking_y0 + parking_height

        fig.add_shape(
            type="rect",
            x0=parking_x0,
            y0=parking_y0,
            x1=parking_x1,
            y1=parking_y1,
            line=dict(width=2),
        )

        fig.add_annotation(
            x=(parking_x0 + parking_x1) / 2,
            y=(parking_y0 + parking_y1) / 2,
            text="Parking",
            showarrow=False,
        )

    # --------------------------------------------------
    # 12. Plot settings
    # --------------------------------------------------

    fig.update_xaxes(
        title="Width (ft)",
        scaleanchor="y",
        scaleratio=1,
    )

    fig.update_yaxes(
        title="Length (ft)",
    )

    fig.update_layout(
        title="Conceptual 2D Floor Plan",
        width=800,
        height=700,
        showlegend=False,
    )

    return fig