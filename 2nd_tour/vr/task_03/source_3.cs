using System;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class RollerBall : MonoBehaviour
{
   public GameObject ViewCamera;
   public bool UseManualBallController;

   private const int IntervalMilliseconds = 25;
   private const float Speed = 4f;

   private Rigidbody mRigidBody;
   private int lastCallTime = -IntervalMilliseconds;
   private int iterations;
   private BallControl ballController;
   private int visitedCoinCount;
   private float successTime;

   private readonly List<Vector2> ballPositions = new List<Vector2>();
   private bool finished;
   private bool success;
   private bool outputWrote;

   private void Start()
   {
      mRigidBody = GetComponent<Rigidbody>();
      Debug.Assert(mRigidBody != null);
      lastCallTime = (int)(Time.time * 1000) + IntervalMilliseconds;
      ballController = UseManualBallController ? (BallControl) new ManualBallControl() : 
         new AutoBallControl();
      try {
         ballController.SetMaze();
      }
      catch (Exception) {
         Application.Quit(1);
      }
      if (MazeDescription.IsConsoleRun())
         Time.timeScale = 100.0f;
   }

   private void Finish()
   {
      finished = true;
      SaveBallPosition();
      Time.timeScale = 1.0f;
      if (MazeDescription.IsConsoleRun()) {
         WriteOutputFile();
         Application.Quit();
      }
   }

   private void WriteOutputFile()
   {
      if (outputWrote)
         return;
      outputWrote = true;
      var lines = new List<string>{
         success ? "Success" : (MazeDescription.Coins - visitedCoinCount).ToString(),
         ballPositions.Count.ToString(),
      };
      foreach (var ballPosition in ballPositions)
         lines.Add(ballPosition.x + " " + ballPosition.y);
      File.WriteAllLines("output.txt", lines.ToArray());
   }

   private void SaveBallPosition()
   {
      ballPositions.Add(new Vector2(transform.position.x, transform.position.z));
   }

   private void FixedUpdate()
   {
      if (visitedCoinCount == MazeDescription.Coins) {
         if (!finished)
            successTime = Time.unscaledTime;
         Debug.Log("Success. Time:  " + successTime);
         success = true;
         Finish();
         return;
      }

      if (iterations == MazeDescription.BallEnergy) {
         Debug.Log("Ball has no energy!");
         success = false;
         Finish();
         return;
      }

		if (true || !MazeDescription.IsConsoleRun()) {
         var stepCount = 0;
         while (Time.time * 1000 + IntervalMilliseconds >= lastCallTime) {
            ++stepCount;
            lastCallTime += IntervalMilliseconds;
         }
         if (stepCount == 0)
            return;
      }

      SaveBallPosition();
      if (mRigidBody != null) {
         int move = 0;
         try {
            move = ballController.GetMove(transform.position.x, transform.position.z);
         }
         catch (Exception) {
            Application.Quit(1);
         }
         var velocity = Vector3.zero;
         if ((move & BallControl.MoveTypeRight) != 0)
            velocity += Vector3.right;
         if ((move & BallControl.MoveTypeBottom) != 0)
            velocity += Vector3.back;
         if ((move & BallControl.MoveTypeLeft) != 0)
            velocity -= Vector3.right;
         if ((move & BallControl.MoveTypeTop) != 0)
            velocity -= Vector3.back;

         mRigidBody.velocity = velocity;
         if (velocity != Vector3.zero)
            mRigidBody.velocity = velocity.normalized * Speed;
         Debug.Log(iterations);
         ++iterations;
      }

      if (ViewCamera != null) {
         var direction = (Vector3.up * 5 + Vector3.back) * 4;
         RaycastHit hit;
         Debug.DrawLine(transform.position,transform.position + direction,Color.red);
         ViewCamera.transform.position =
            Physics.Linecast(transform.position, transform.position + direction, out hit)
               ? hit.point
               : transform.position + direction;
         ViewCamera.transform.LookAt(transform.position);
      }
   }

   private void OnTriggerEnter(Collider other)
   {
      if (other.gameObject.tag.Equals("Coin")) {
         Destroy(other.gameObject);
         ++visitedCoinCount;
      }
   }
}