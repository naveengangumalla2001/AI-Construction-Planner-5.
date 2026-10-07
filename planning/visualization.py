import plotly.graph_objects as go


def add_box(
    fig,
    x0,
    x1,
    y0,
    y1,
    z0,
    z1,
    name="Building",
    color="lightblue"
):

    vertices = [
        (x0, y0, z0),
        (x1, y0, z0),
        (x1, y1, z0),
        (x0, y1, z0),

        (x0, y0, z1),
        (x1, y0, z1),
        (x1, y1, z1),
        (x0, y1, z1)
    ]

    x = [v[0] for v in vertices]
    y = [v[1] for v in vertices]
    z = [v[2] for v in vertices]

    faces = [
        (0, 1, 2),
        (0, 2, 3),

        (4, 5, 6),
        (4, 6, 7),

        (0, 1, 5),
        (0, 5, 4),

        (1, 2, 6),
        (1, 6, 5),

        (2, 3, 7),
        (2, 7, 6),

        (3, 0, 4),
        (3, 4, 7)
    ]

    i = [f[0] for f in faces]
    j = [f[1] for f in faces]
    k = [f[2] for f in faces]

    fig.add_trace(
        go.Mesh3d(
            x=x,
            y=y,
            z=z,
            i=i,
            j=j,
            k=k,
            color=color,
            opacity=0.75,
            name=name,
            hovertext=name,
            hoverinfo="text"
        )
    )


def add_window(
    fig,
    x,
    y,
    z,
    width=5,
    height=4
):

    fig.add_trace(
        go.Mesh3d(
            x=[
                x,
                x + width,
                x + width,
                x
            ],

            y=[
                y,
                y,
                y,
                y
            ],

            z=[
                z,
                z,
                z + height,
                z + height
            ],

            i=[0, 0],
            j=[1, 2],
            k=[2, 3],

            color="darkblue",
            opacity=1,

            name="Window",

            hovertext="Window",
            hoverinfo="text"
        )
    )


def add_door(
    fig,
    x,
    y,
    z,
    width=4,
    height=7
):

    fig.add_trace(
        go.Mesh3d(

            x=[
                x,
                x + width,
                x + width,
                x
            ],

            y=[
                y,
                y,
                y,
                y
            ],

            z=[
                z,
                z,
                z + height,
                z + height
            ],

            i=[0, 0],
            j=[1, 2],
            k=[2, 3],

            color="brown",
            opacity=1,

            name="Door",

            hovertext="Main Door",
            hoverinfo="text"
        )
    )


def create_3d_building(
    plot_area,
    builtup_area,
    floors,
    bedrooms,
    bathrooms,
    parking="No"
):

    fig = go.Figure()

    # -----------------------------------------------------
    # Approximate building dimensions
    # -----------------------------------------------------

    width = 40
    length = 45

    floor_height = 10

    # -----------------------------------------------------
    # Create floors
    # -----------------------------------------------------

    for floor in range(int(floors)):

        z0 = floor * floor_height
        z1 = z0 + floor_height

        # Building slab
        add_box(
            fig,
            0,
            width,
            0,
            length,
            z0,
            z1,
            name=f"Floor {floor + 1}",
            color="lightblue"
        )

        # -------------------------------------------------
        # Windows
        # -------------------------------------------------

        window_z = z0 + 3

        # Front windows
        for x in [5, 17, 29]:

            add_window(
                fig,
                x,
                0,
                window_z,
                width=5,
                height=4
            )

        # Right-side windows
        add_window(
            fig,
            width,
            10,
            window_z,
            width=0.1,
            height=4
        )

    # -----------------------------------------------------
    # Main entrance door
    # -----------------------------------------------------

    add_door(
        fig,
        18,
        0,
        0,
        width=5,
        height=7
    )

    # -----------------------------------------------------
    # Roof
    # -----------------------------------------------------

    roof_z = int(floors) * floor_height

    add_box(
        fig,
        -1,
        width + 1,
        -1,
        length + 1,
        roof_z,
        roof_z + 1,
        name="Roof",
        color="gray"
    )

    # -----------------------------------------------------
    # Parking area
    # -----------------------------------------------------

    # Parking is shown as a conceptual area.
    # This does not affect the building structure.

    parking_width = 15
    parking_length = 18

    add_box(
        fig,
        0,
        parking_width,
        -parking_length,
        0,
        0,
        0.5,
        name="Parking",
        color="lightgray"
    )

    # -----------------------------------------------------
    # Layout
    # -----------------------------------------------------

    fig.update_layout(

        title="🏠 3D Building Visualization",

        scene=dict(

            xaxis_title="Width (ft)",

            yaxis_title="Length (ft)",

            zaxis_title="Height (ft)",

            aspectmode="data",

            camera=dict(
                eye=dict(
                    x=1.6,
                    y=1.6,
                    z=1.3
                )
            )
        ),

        margin=dict(
            l=0,
            r=0,
            t=50,
            b=0
        ),

        height=700
    )

    return fig