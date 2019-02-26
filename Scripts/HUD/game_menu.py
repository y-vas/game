


def menu(L):
    camera = L.getCurrentScene().active_camera

    # A sphere of radius 4.0 located at [x, y, z] = [1.0, 1.0, 1.0]
    if (camera.sphereInsideFrustum([1.0, 1.0, 1.0], 4) != camera.OUTSIDE):
        print("dfasdf")
