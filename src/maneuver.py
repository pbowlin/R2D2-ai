import math
import time

# -----------------------------------------
# Following are copied from maneuver.py
def follow_path(droid_client, path):
    """Helper function to move droid client via vertex path specified.
     Return True if succssful, False otherwise.
    """
    #speed, scale_dist = 0x48, 1
    roll_speed = 0.37
    roll_time = 1

    cur_pos = path[0]
    for next_pos in path[1:]:

        # compute distance and angle to next position
        print('%s -> %s' % (cur_pos, next_pos))

        #dist, ang = self.__compute_roll_parameters(cur_pos, next_pos)
        #rolled = self.__roll(droid_client, speed, ang, dist*scale_dist)
        #if not rolled:
            #print('Something went wrong.')
            #return False

        #cur_pos = next_pos
    #print('Path complete.')
    #return True


        x_diff = next_pos[0] - cur_pos[0]
        y_diff = next_pos[1] - cur_pos[1]

        if x_diff > 0:
            heading = 0
        elif x_diff < 0:
            heading = 180
        elif y_diff > 0:
            heading = 270
        else:
            heading = 90
        rolled = __roll(droid_client, roll_speed, heading, roll_time)

        cur_pos = next_pos
    return True

def __roll(droid_client, speed, ang, time):
    """Helper function to move droid. Use follow_path() instead."""
    return droid_client.roll(speed, ang, time)




'''
def follow_path(sphero, path, speed, scale_dist=1):

    cur_pos = path[0]
    for next_pos in path[1:]:

        # compute distance and angle to next position
        # print('%s -> %s' % (cur_pos, next_pos))
        dist, ang = compute_roll_parameters(cur_pos, next_pos)
        rolled = roll(sphero, speed, ang, dist*scale_dist)
        if not rolled:
            print('Something went wrong.')
            return False

        cur_pos = next_pos
    # print('Path complete.')
    return True

def roll(sphero, speed, ang, time):
    return sphero.roll(speed, ang, time)

def compute_roll_parameters(old_pos, new_pos):

    x_1, y_1 = old_pos
    x_2, y_2 = new_pos
    d_x, d_y = (x_2 - x_1), (y_2 - y_1)

    dist = math.sqrt(d_x**2 + d_y**2)
    ang = 90 - math.atan2(d_y, d_x) * (180/math.pi)

    return dist, ang

'''
