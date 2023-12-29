import numpy as np
import PCL

def generate_point_cloud(self):
    # Assuming self.cartesian contains the cartesian coordinates
    if self.cartesian is not None:
        # Convert the cartesian coordinates to a numpy array
        cartesian_np = np.array(self.cartesian, dtype=np.float32)

        # Create a point cloud object
        cloud = PCL.PointCloud()

        # Set the points of the cloud to the cartesian coordinates
        cloud.from_array(cartesian_np)

        return cloud