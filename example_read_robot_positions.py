#!/usr/bin/python3

# This example shows how to read periodically the joint angles and the position of the robot.
# Use Ctrl+C to stop the program

import websocket # websocket-client https://github.com/websocket-client/websocket-client
import json      # default supported by python

# Each message which is received through the WebSocket is processed in this function
def on_message(ws, message):
    msg = json.loads(message) # Convert json to python dictionary for easier usage

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

    # Auth service call needs to be set directly on the first request after established connection
    auth_service = {
        "op": "auth",
        "client": "my-client",
        "dest": "ros",
        "end": 0,
        "level": "admin",
        "mac": MAC_AUTH,
        "rand": "rand",
        "t": 0
    }
    ws.send(json.dumps(auth_service))

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
