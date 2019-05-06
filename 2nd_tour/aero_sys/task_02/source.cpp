#include <Servo.h> 
#include <ros.h>
#include <std_msgs/Int32.h>

Servo servo;

std_msgs::Int32 value_msg;

ros::NodeHandle nh;
ros::Publisher pub("/servo_cmd_echo", &value_msg);

void servo_cb( const std_msgs::Int32& cmd_msg)
{
  servo.write(cmd_msg.data); //set servo angle, should be from 0-180  

  value_msg.data = cmd_msg.data;
  pub.publish( &value_msg );
}

ros::Subscriber<std_msgs::Int32> sub("/servo_cmd", servo_cb);

void setup()
{
  servo.attach(9);
  servo.write(90);
  
  nh.initNode();
  nh.subscribe(sub);
  nh.advertise(pub);
}

void loop(){
  nh.spinOnce();
  delay(1);
}