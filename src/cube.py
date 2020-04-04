
class cube():
    size = 0.5
    sizef = size * 2

    faces = [
        ( 0, 1, 0),
        ( 0,-1, 0),
        (-1, 0, 0),
        ( 1, 0, 0),
        ( 0, 0, 1),
        ( 0, 0,-1),
    ]

    @staticmethod
    def get(self, type = 'grass'):

        dict = {
            'grass': cube.tex_coords((1, 0), (0, 1), (0, 0)),
            'sand' : cube.tex_coords((1, 1), (1, 1), (1, 1)),
            'brick': cube.tex_coords((2, 0), (2, 0), (2, 0)),
            'stone': cube.tex_coords((2, 1), (2, 1), (2, 1))
        }

        return dict[type]

    @classmethod
    def vertices(self,x, y, z):
        """ Return the vertices of the cube at position x, y, z with size 2*n. """
        n = self.size

        return [
            x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n,  # top
            x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # bottom
            x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n,  # left
            x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n,  # right
            x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n,  # front
            x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n,  # back
        ]

    @staticmethod
    def tex_coord(x, y, n = 4):
        """ Return the bounding vertices of the texture square """
        m = 1.0 / n
        dx = x * m
        dy = y * m
        return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m

    @staticmethod
    def tex_coords(top, bottom, side):
        """ Return a list of the texture squares for the top, bottom and side """
        top = cube.tex_coord(*top)
        bottom = cube.tex_coord(*bottom)
        side = cube.tex_coord(*side)
        result = []
        result.extend(top)
        result.extend(bottom)
        result.extend(side * 4)
        return result
