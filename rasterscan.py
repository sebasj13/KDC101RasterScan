from re import A

import numpy as np
from pylablib.devices import Thorlabs
from tqdm import tqdm

AXIAL_MOTOR_ID = "27003287"
TRANSVERSAL_MOTOR_ID = "27001138"

try:
    axial_stage = Thorlabs.KinesisMotor(AXIAL_MOTOR_ID, scale="stage")
except Exception:
    print("Axial stage not found")

try:
    transversal_stage = Thorlabs.KinesisMotor(TRANSVERSAL_MOTOR_ID, scale="stage")
except Exception:
    print("Transversal stage not found")


def RasterScan(cols, rows, colstep, rowstep, start=(0, 0)):

    a, b = ramp_arrays(cols, rows)
    print(f"Moving to starting position: {start[0]}, {start[1]} ...\n")
    axial_stage.move_to(start[0])
    transversal_stage.move_to(start[1])

    a = a * colstep
    b = b * rowstep
    while True:
        if axial_stage.is_moving() == False and transversal_stage.is_moving() == False:
            print(f"Running {cols}x{rows} scan ...\n")
            break
    for i in tqdm(range(len(a))):
        axial_stage.move_to(a[i] + start[0])
        transversal_stage.move_to(b[i] + start[1])
        axial_stage.wait_for_stop()
        transversal_stage.wait_for_stop()
    print("\n\nScan completed! Moving back to start position ...\n")
    axial_stage.move_to(start[0])
    transversal_stage.move_to(start[1])
    while True:
        if axial_stage.is_moving() == False and transversal_stage.is_moving() == False:
            print("Done!", end="")
            break
    return


def ramp_arrays(cols, rows):
    a = [[] for i in range(rows)]
    for i in range(rows):
        for j in range(cols):
            a[i] += [i]

    a = np.array(a).flatten()

    b = [[] for i in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if i % 2 != 0:
                b[i] += [cols - j - 1]
            else:
                b[i] += [j]

    b = np.array(b).flatten()
    return a, b
