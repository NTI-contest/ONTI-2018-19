import java.net.*;
import java.io.*;
import java.math.*;
class Tracking {
    public static void main(String args[])
    throws Exception{
    Client client = new Client();
    int speed = 1;
    int dir = 1;
    int dx;
    int abs_dx;
    client.start();
    client.left(1);
    Thread.sleep(1000);
    client.right(speed);
    for (int i = 0; i < 10; i = 0) // in fact - infinite loop, to fix smart java compiler
    {
        while (!client.readstatus()) {
            System.out.println("not ready");
            Thread.sleep(100);
            client.readstatus();
        }
        dx = (int)client.getDx();
        abs_dx = Math.abs(dx);
        // System.out.print("dx: "); System.out.println(dx);
        if (dx < 500 && dx > -500) {
            speed = 1;
            if (dx < 30 && dx > -30) {
                client.stop();
                // System.out.println("stop");
            }
            else {
                speed = abs_dx / 20;
                // System.out.print("move: ");
                // System.out.print(speed);
                if (dx < 0) {
                    client.right(speed);
                    // System.out.println("right ");
                }
                if (dx > 0) {
                    client.left(speed);
                    // System.out.println("left ");
                }
            }
        }
        else {
            speed = 0;
            // System.out.println("DO NOTHING - CAN NOT SEE");
        }
        //search if lost
        if (client.ifPositionRight()) {
            speed = 10;
            client.left(speed);
            // System.out.println("LOST, SEARCH LEFT");
        }
        if (client.ifPositionLeft()) {
            speed = 10;
            client.right(speed);
            // System.out.println("LOST, SEARCH RIGHT");
        }
        Thread.sleep(10);
    }
    client.quit();
    client.stop();
}
}