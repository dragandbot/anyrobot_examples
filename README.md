# anyrobot_examples

Examples for the AnyRobot Interface

# Requirements

AnyRobot Interface must be running locally inside a drag&bot runtime instance. Examples cannot be run without the interface.
drag&bot Robot Simulator must be running with a Simbot selected.

# Installation

1. Install a Python 3 environment in your linux computer.
2. Clone the repository
3. Install the required python packages.
4. Execute each example using python3 command: e.g. python3 read_robot_joints.py

## Package dependencies

The following python packages are required: websocket-client

You can install the packages using pip3 tool, assuming pip is already installed in your linux system.
E.g.: pip3 install websocket-client

# Examples execution

Execute the corresponding test in linux terminal: e.g. python3 read_robot_joints.py

# Example / Tools list

1. example_read_robot_positions.py

This example connects to the AnyRobot Interface and starts receiving joint and tool positions. These values are printed in the console.

Trace in console looks similar to:

Robot position as Euler Intrinsic ZYX frame (m, radians): {'x': 0.5015877485275269, 'y': 2.310114979309219e-07, 'z': 0.7040988206863403, 'alpha': -3.141592264175415, 'beta': 0.01039330754429102, 'gamma': 3.141591787338257}
Joint positions in radians: [0.0, 0.0908, 1.5708, 0.0, 1.4696, 0.0]

2. example_move_robot.py

This example moves the robot up and down one time while printing its joints in a similar way to the previous example.

3. example_ios.py

This example reads value of digital output number one, sets its value to the opposite one, and read it the value again.

Expected trace:

python3 example_ios.py 
Digital Output original value: False
Digital Output current value: True

# Documentation for websocket in python

https://github.com/websocket-client/websocket-client

There two ways to use the websocket client:
- synchronous: send and request are processed sequentially. After each send, recv is following. This paradigm can be used with service calls.
- asynchronous: messages are received continuously. This paradigm triggers a processing function each time a message is received in the websocket.

It is possible to combine more than one socket connection for commodity. Also it is possible to use threading for combining both paradigms in a program using asynchronous socket connection (WebSocketApp) and message id identification.

# Documentation for RosBridge encapsulation

https://github.com/RobotWebTools/rosbridge_suite/blob/ros1/ROSBRIDGE_PROTOCOL.md