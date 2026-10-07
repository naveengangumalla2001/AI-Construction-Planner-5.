import plotly.graph_objects as go


def create_3d_building(
    plot_area,
    builtup_area,
    floors,
    bedrooms,
    bathrooms
):
    """
    Create a conceptual 3D building visualization.
    This is for preliminary planning only.
    """

    # -------------------------------------------------
    # Approximate building dimensions
    # -------------------------------------------------

    width = min(45, (builtup_area ** 0.5) * 0.9)
    length = min(45, (builtup_area ** 0.5) * 1.1)

    floor_height = 10

    fig = go.Figure()

    # -------------------------------------------------
    # Building floors
    # -------------------------------------------------

    for floor in range(floors):

        z = floor * floor_height

        # Floor slab
        fig.add_trace(
            go.Mesh3d(
                x=[
                    0, width, width, 0,
                    0, width, width, 0
                ],
                y=[
                    0, 0, length, length,
                    0, 0, length, length
                ],
                z=[
                    z, z, z, z,
                    z + 0.3, z + 0.3,
                    z + 0.3, z + 0.3
                ],
                i=[0, 0, 0, 4, 4, 4],
                j=[1, 2, 3, 5, 6, 7],
                k=[2, 3, 4, 6, 7, 5],
                opacity=0.35,
                name=f"Floor {floor + 1}"
            )
        )

        # -------------------------------------------------
        # Front windows
        # -------------------------------------------------

        window_positions = [0.20, 0.45, 0.70]

        for position in window_positions:

            x = width * position

            fig.add_trace(
                go.Mesh3d(
                    x=[
                        x - 2,
                        x + 2,
                        x + 2,
                        x - 2
                    ],
                    y=[
                        -0.2,
                        -0.2,
                        -0.2,
                        -0.2
                    ],
                    z=[
                        z + 3,
                        z + 3,
                        z + 6,
                        z + 6
                    ],
                    i=[0, 0],
                    j=[1, 2],
                    k=[2, 3],
                    opacity=0.9,
                    name="Window"
                )
            )

    # -------------------------------------------------
    # Roof
    # -------------------------------------------------

    roof_z = floors * floor_height

    fig.add_trace(
        go.Mesh3d(
            x=[
                0,
                width,
                width,
                0
            ],
            y=[
                0,
                0,
                length,
                length
            ],
            z=[
                roof_z,
                roof_z,
                roof_z,
                roof_z
            ],
            i=[0, 0],
            j=[1, 2],
            k=[2, 3],
            opacity=0.7,
            name="Roof"
        )
    )

    # -------------------------------------------------
    # Main Door
    # -------------------------------------------------

    door_width = 4
    door_height = 7

    fig.add_trace(
        go.Mesh3d(
            x=[
                width / 2 - door_width / 2,
                width / 2 + door_width / 2,
                width / 2 + door_width / 2,
                width / 2 - door_width / 2
            ],
            y=[
                -0.3,
                -0.3,
                -0.3,
                -0.3
            ],
            z=[
                0,
                0,
                door_height,
                door_height
            ],
            i=[0, 0],
            j=[1, 2],
            k=[2, 3],
            opacity=1,
            name="Main Door"
        )
    )

    # -------------------------------------------------
    # Layout
    # -------------------------------------------------

    fig.update_layout(
        title="🏠 3D Building Visualization",

        scene=dict(

            xaxis_title="Width (ft)",

            yaxis_title="Length (ft)",

            zaxis_title="Height (ft)",

            aspectmode="manual",

            aspectratio=dict(
                x=1,
                y=1,
                z=0.8
            )
        ),

        height=700,

        margin=dict(
            l=0,
            r=0,
            t=50,
            b=0
        )
    )

    return fig