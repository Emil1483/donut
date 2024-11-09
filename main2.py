import numpy as np

screen_size = 20, 10
width, height = screen_size

illumination = np.fromiter(".,-~:;=!*#$@", dtype="<U1")

def render_scene(points: np.ndarray, z_offset = 5.0, camera_distance=25.0) -> None:
    n, dimensions = points.shape

    assert dimensions == 3, "Points must be 3D"

    pixels = np.full(screen_size, " ")
    zbuffer = np.zeros(screen_size)

    x, y, z = points.T
    ooz = np.reciprocal(z + z_offset)

    xp = (camera_distance * x * ooz + width / 2).astype(int)
    yp = (-camera_distance * y * ooz / 1.5 + height / 2).astype(int)

    for n in range(n):
        # pixels[xp[n], yp[n]] = "@"
        pixels[xp[n], yp[n]] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[n]
    
    print(*["".join(row) for row in pixels.T], sep="\n")

def cube() -> np.ndarray:
    points = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 1, 1]
    ])

    return points.astype(float)

def rotate(theta: float, phi: float) -> np.ndarray:
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    cos_phi = np.cos(phi)
    sin_phi = np.sin(phi)

    rotation_matrix = np.array([
        [cos_theta, -sin_theta, 0],
        [sin_theta * cos_phi, cos_theta * cos_phi, -sin_phi],
        [sin_theta * sin_phi, cos_theta * sin_phi, cos_phi]
    ])

    return rotation_matrix

if __name__ == "__main__":

    theta = 0

    while True:
        points = (cube() - np.array([0.5, 0.5, 0.5])) * 4
        for n in range(len(points)):
            points[n] = rotate(theta, np.pi / 3 ).dot(points[n])

        print("\x1b[H")
        render_scene(points, z_offset=15.0)

        theta += 0.0015