#!/usr/bin/python3

# This example shows how to read periodically the joint angles and the joint position of the robot.
# Use Ctrl+C to stop the program 

# dnb_tool_frame --> includes robot tool in drag&bot
# tool_frame --> tool configured directly in robot controller, usually flange.

import websocket # websocket-client https://github.com/websocket-client/websocket-client
import json      # default support python

# Returns a joint motion command with two waypoints (two joint positions)
def create_move_command():
    payload = {
        "commands": [
            {   "command_type": "PTP", 
                "pose_type": "JOINTS",
                "pose": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                "velocity_type": "RAD/S",
                "velocity": [0.1],
                "acceleration_type": "RAD/S^2",
                "acceleration": [1.0],
                "blending_type": "%",
                "blending": [0.0]
            },
            {   "command_type": "PTP", 
                "pose_type": "JOINTS",
                "pose": [1.0, 1.0, 1.0, -1.0, -1.0, -1.0],
                "velocity_type": "RAD/S",
                "velocity": [0.1],
                "acceleration_type": "RAD/S^2",
                "acceleration": [1.0],
                "blending_type": "%",
                "blending": [0.0]
            },
        ]
    }
    command = {
        "op": "publish",
        "topic": "/command_list",
        "msg": payload
    }
    return json.dumps(command)

# Each message which is received through the WebSocket is processed in this function
def on_message(ws, message):
    msg = json.loads(message)
    if msg["op"] == "publish":
        if msg["topic"] == "/joint_states":
            any_robot_interface_payload = msg["msg"]
            print("Joint positions in radians: " + str(any_robot_interface_payload["position"]))
        elif msg["topic"] == "/tool_frame":
            any_robot_interface_payload = msg["msg"]
            print("Robot position as Euler Intrinsic ZYX frame (m, radians): " + str(any_robot_interface_payload))

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("Closed connection to AnyRobot Interface")

def on_open(ws):
    print("Opened connection to AnyRobot Interface")
    # Activate subscription to joint_states topic for getting the joint values
    msg_subscribe_joint_command = {
        "op": "subscribe",
        "topic": "/joint_states"}	
    ws.send(json.dumps(msg_subscribe_joint_command)) # Send command to AnyRobot Interface
    # Activate subscription to get robot pose
    msg_subscribe_joint_command = {
        "op": "subscribe",
        "topic": "/tool_frame"}	
    ws.send(json.dumps(msg_subscribe_joint_command)) # Send command to AnyRobot Interface

    # Send a move containing two waypoints
    command_move_robot = create_move_command()
    ws.send(command_move_robot)
    

if __name__ == "__main__":
    connection_ip = "127.0.0.1" # Loopback localhost address, assuming running in same computer
    connection_port = 9091
    connection_uri = "ws://" + connection_ip + ":" + str(connection_port)

    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(connection_uri, 
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close)

    ws.run_forever()