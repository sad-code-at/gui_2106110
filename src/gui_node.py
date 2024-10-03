#!/usr/bin/env python3
import tkinter as tk
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import time


meulas_label = None
message_label = None
root = None
pub = rospy.Publisher("/turtle1/cmd_vel",Twist, queue_size=10)

# Global variable to track the remaining meulas
meulas = 10
flag_forward = False #flag_variables
flag_backward = False
# Function to update the remaining meulas label
def update_meulas_label():
    meulas_label.config(text=f"Remaining Meulas: {meulas}")

# Function to update the message label
def update_message(msg):
    message_label.config(text=f"Message: {msg}")

# Function for moving the bot forward
def move_forward():
    global flag_forward
    global flag_backward
    flag_forward = True
    flag_backward = False
    move_linear()

# Function for moving the bot backward
def move_back():
    global flag_backward
    global flag_forward
    flag_backward = True
    flag_forward = False
    move_linear()

def move_linear():
    global flag_forward
    global flag_backward
    t0 = rospy.Time.now().to_sec()
    def update_linear_velocity():
        global meulas
        nonlocal t0
        if flag_forward == True and meulas >=1 :
            msg = Twist()
            msg.linear.x = 2
            pub.publish(msg)
            t1 =rospy.Time.now().to_sec()
            duration = t1-t0
            if duration >=1:
                meulas -= 1
                update_meulas_label()
                t0 = rospy.Time.now().to_sec()
            update_message("Bot is moving forward")
            root.after(100,update_linear_velocity)
        if flag_backward == True and meulas >=1 :
            msg = Twist()
            msg.linear.x = -2
            pub.publish(msg)
            t1 =rospy.Time.now().to_sec()
            duration = t1-t0
            if duration >=1:
                meulas -= 1
                update_meulas_label()
                t0 = rospy.Time.now().to_sec()
            update_message("Bot is moving Back")
            root.after(100,update_linear_velocity)
        elif  meulas == 0 and (flag_forward or flag_backward):
            msg = Twist()
            msg.linear.x = 0
            msg.angular.z = 0
            pub.publish(msg)
            update_message("Error: Not enough meulas!")
            root.after(100,update_linear_velocity)       
    update_linear_velocity()          


# Function for turning the bot left
def move_left():
    global meulas
    global flag_forward
    global flag_backward
    flag_forward = False
    flag_backward = False
    msg = Twist()
    if meulas >= 2:
        meulas -= 2
        update_meulas_label()
        t0 = rospy.Time.now().to_sec()
        t1 = 0
        displacement = 0
        while displacement <= 3.1416/2:
            msg.angular.z = +0.5
            pub.publish(msg)
            t1 = rospy.Time.now().to_sec()
            duration = (t1-t0)
            displacement = duration*0.5
        msg.angular.z = 0
        pub.publish(msg)    
        update_message("Bot is moving Left")
    else:
        msg.linear.x = 0
        msg.angular.z = 0
        pub.publish(msg)        
        update_message("Error: Not enough meulas!")

# Function for turning the bot right
def move_right():
    global meulas
    global flag_forward
    global flag_backward
    flag_forward = False
    flag_backward = False
    msg = Twist()
    if meulas >= 2:
        meulas -= 2
        update_meulas_label()
        t0 = rospy.Time.now().to_sec()
        t1 = 0
        displacement = 0
        while displacement <= 3.1416/2:
            msg.angular.z = -0.5
            pub.publish(msg)
            t1 = rospy.Time.now().to_sec()
            duration = (t1-t0)
            displacement = duration*0.5
        msg.angular.z = 0
        pub.publish(msg)       
        update_message("Bot is moving Right")
    else:
        msg.linear.x = 0
        msg.angular.z = 0
        pub.publish(msg)        
        update_message("Error: Not enough meulas!")

# Function to increase meulas
def increase_meulas():
    global meulas
    global flag_forward
    global flag_backward
    flag_forward = False
    flag_backward = False
    msg = Twist()
    meulas += 10
    t0 = rospy.Time.now().to_sec()
    t1 = 0
    displacement = 0
    while displacement <= 2*3.1416:
        msg.angular.z = 2
        pub.publish(msg)
        t1 = rospy.Time.now().to_sec()
        duration = (t1-t0)
        displacement = duration*2

    msg.angular.z = 0
    pub.publish(msg)    
    update_meulas_label()
    update_message("Meulas Increased")


def control_robot():
    # initialising node
    rospy.init_node("gui_node", anonymous=True)
    rate = rospy.Rate(10)    

    # Create the main window
    global root
    root = tk.Tk()
    root.title("TurtleBot GUI")
    root.geometry("600x400")
    root.minsize(300,400)

    # Meulas Label
    global meulas_label
    global message_label
    meulas_label = tk.Label(root, text="Remaining Meulas: 10")
    meulas_label.grid(row=0, column=5)

    # Buttons for controlling the bot
    forward_button = tk.Button(root, text="Forward", command=move_forward)
    back_button = tk.Button(root, text="Back", command=move_back)
    left_button = tk.Button(root, text="Left", command=move_left)
    right_button = tk.Button(root, text="Right", command=move_right)
    increase_button = tk.Button(root, text="Increase Meulas", command=increase_meulas)

    # Place buttons on the grid
    forward_button.grid(row=0, column=1)
    left_button.grid(row=1, column=0)
    back_button.grid(row=2, column=1)
    right_button.grid(row=1, column=2)
    increase_button.grid(row=1, column=5)

    # Message Label
    message_label = tk.Label(root, text="Message: Bot is waiting")
    message_label.grid(row=4, column=3, columnspan=3)

    # Start the Tkinter event loop
    root.mainloop()


if __name__== "__main__": 
    try: 
        control_robot()
    except rospy.ROSInterruptException:
        pass    
