import numpy as np
from blessed import Terminal

illumination = np.fromiter(".,-~:;=!*#$@", dtype="<U1")


def render_scene(
    term: Terminal,
    points: np.ndarray,
    z_offset=5.0,
    camera_distance=25.0,
):
    n, dimensions = points.shape

    assert dimensions == 3, "Points must be 3D"

    screen_size = term.width // 1, term.height - 1
    width, height = screen_size

    pixels = np.full(screen_size, " ")
    zbuffer = np.zeros(screen_size)

    x, y, z = points.T
    ooz = np.reciprocal(z + z_offset)

    xp = (camera_distance * x * ooz + width / 2).astype(int)
    yp = (-camera_distance * y * ooz / 1.5 + height / 2).astype(int)

    for n in range(n):
        # pixels[xp[n], yp[n]] = "@"
        pixels[xp[n], yp[n]] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[n]

    with term.location(0, 0):
        print(*["".join(row) for row in pixels.T], sep="\n")


def cube() -> np.ndarray:
    points = np.array(
        [
            [0, 0, 0],
            [1, 0, 0],
            [1, 1, 0],
            [0, 1, 0],
            [0, 0, 1],
            [1, 0, 1],
            [1, 1, 1],
            [0, 1, 1],
        ]
    )

    return points.astype(float)


# def rotate(theta: float, phi: float) -> np.ndarray:
#     cos_theta = np.cos(theta)
#     sin_theta = np.sin(theta)
#     cos_phi = np.cos(phi)
#     sin_phi = np.sin(phi)

#     rotation_matrix = np.array(
#         [
#             [cos_theta, -sin_theta, 0],
#             [sin_theta * cos_phi, cos_theta * cos_phi, -sin_phi],
#             [sin_theta * sin_phi, cos_theta * sin_phi, cos_phi],
#         ]
#     )

#     return rotation_matrix


def rotate(theta: float, axis: np.ndarray) -> np.ndarray:
    axis = axis / np.linalg.norm(axis)
    a, b, c = axis
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    rotation_matrix = np.array(
        [
            [
                a * a + (1 - a * a) * cos_theta,
                a * b * (1 - cos_theta) - c * sin_theta,
                a * c * (1 - cos_theta) + b * sin_theta,
            ],
            [
                a * b * (1 - cos_theta) + c * sin_theta,
                b * b + (1 - b * b) * cos_theta,
                b * c * (1 - cos_theta) - a * sin_theta,
            ],
            [
                a * c * (1 - cos_theta) - b * sin_theta,
                b * c * (1 - cos_theta) + a * sin_theta,
                c * c + (1 - c * c) * cos_theta,
            ],
        ]
    )

    return rotation_matrix


if __name__ == "__main__":
    term = Terminal()

    points = 4 * (cube() - np.array([0.5, 0.5, 0.5]))

    rotation = rotate(0.0005, np.array([0, 1, 0]))

    with term.fullscreen(), term.hidden_cursor():
        while True:
            for n in range(len(points)):
                points[n] = rotation.dot(points[n])

            render_scene(term, points, z_offset=10.0)
