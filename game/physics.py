import numpy as np

def elastic2DCollision(entity1, entity2, vel1, vel2, dir1, dir2, contanct_dir):
    """Simulates elastic collision between two circles in 2D
    
    Arguments:
        entity1  -- first colliding object
        entity2  -- second colliding object
        vel1  -- absolute velocity value of first object
        vel2  -- absolute velocity value of second object
        dir1  -- vector representing the direction the first object is going
        dir2 --  vector representing the direction the second object is going
        contanct_dir  -- vector representing the direction from center of first object to contact point
    """
    mass_diff = entity1.weight - entity2.weight
    mass_sum = entity1.weight + entity2.weight

    #Current velocities in the collision reference frame
    v1_x = vel1 * np.cos(dir1 - contanct_dir)
    v1_y = vel1 * np.sin(dir1 - contanct_dir)
    v2_x = vel2 * np.cos(dir2 - contanct_dir)
    v2_y = vel2 * np.sin(dir2 - contanct_dir)

    #Calc new velocities in the collision reference frame using conservation of momentum
    v1_new_x = (mass_diff * v1_x + 2 * entity2.weight * v2_x) / mass_sum
    v1_new_y = v1_y
    v2_new_x = (-mass_diff * v2_x + 2 * entity1.weight * v1_x) / mass_sum
    v2_new_y = v2_y

    #Convert to normal reference frame
    entity1_new_vx = np.cos(contanct_dir) * v1_new_x + np.cos(contanct_dir + np.pi / 2) * v1_new_y
    entity1_new_vy = np.sin(contanct_dir) * v1_new_x + np.sin(contanct_dir + np.pi / 2) * v1_new_y
    entity2_new_vx = np.cos(contanct_dir) * v2_new_x + np.cos(contanct_dir + np.pi / 2) * v2_new_y
    entity2_new_vy = np.sin(contanct_dir) * v2_new_x + np.sin(contanct_dir + np.pi / 2) * v2_new_y

    entity1.velocity = np.array([entity1_new_vx, entity1_new_vy])
    entity2.velocity = np.array([entity2_new_vx, entity2_new_vy])


