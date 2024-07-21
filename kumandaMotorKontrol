//Receiver signal pins
int ch1_pin = 31;  //PWM pin for forward/backward
int ch2_pin = 33;  //PWM pin for right/left

//Right motor driver pins
int R_EN_right = 2; 
int L_EN_right = 5;
int R_PWM_right = 3; //PWM pin
int L_PWM_right = 6; //PWM pin

//Left motor driver pins
int R_EN_left = 8; 
int L_EN_left = 11;
int R_PWM_left = 9; //PWM pin
int L_PWM_left = 12; //PWM pin

// ---**---   Rx threshold values - Update based on your TX values
//FWD
int Ch1_start_Fwd = 1530;
int Ch1_End_Fwd = 1980;
//BACK
int Ch1_start_Bac = 1460;
int Ch1_End_Bac = 960;
//RIGHT
int Ch2_start_Right = 1500;
int Ch2_End_Right = 1990;
//LEFT
int Ch2_start_Left = 1460;
int Ch2_End_Left = 950;

// ---------***---------------***----------

void setup()
{
  Serial.begin(9600);
  pinMode(ch1_pin, INPUT);
  pinMode(ch2_pin, INPUT);
  
  pinMode(R_EN_right, OUTPUT);
  pinMode(L_EN_right, OUTPUT);
  pinMode(R_PWM_right, OUTPUT);
  pinMode(L_PWM_right, OUTPUT); 
  pinMode(R_EN_left, OUTPUT);
  pinMode(L_EN_left, OUTPUT);
  pinMode(R_PWM_left, OUTPUT);
  pinMode(L_PWM_left, OUTPUT);
}

void loop()
{
  //Receiver signal pins data
  double ch1 = pulseIn(ch1_pin, HIGH);
  double ch2 = pulseIn(ch2_pin, HIGH);

  Serial.print("ch1: ");
  Serial.println(ch1);
  Serial.print("ch2: ");
  Serial.println(ch2);

  //Speed mapping for motors
  int spdFwd = map(ch1, Ch1_start_Fwd, Ch1_End_Fwd, 0, 255);   
  int spdBac = map(ch1, Ch1_start_Bac, Ch1_End_Bac, 0, 255);    
  int spdRight = map(ch2, Ch2_start_Right, Ch2_End_Right, 0, 255);
  int spdLeft = map(ch2, Ch2_start_Left, Ch2_End_Left, 0, 255);

  digitalWrite(R_EN_right, HIGH);
  digitalWrite(L_EN_right, HIGH);
  digitalWrite(R_EN_left, HIGH);
  digitalWrite(L_EN_left, HIGH);

  // Reset motor speeds
  analogWrite(R_PWM_right, 0);
  analogWrite(L_PWM_right, 0);
  analogWrite(R_PWM_left, 0);
  analogWrite(L_PWM_left, 0);

  if (ch1 == 0 && ch2 == 0)
  {
    // Do nothing, stay stopped
  }
  else
  {
    // Handle forward and backward movement
    if (ch1 > Ch1_start_Fwd)
    {
      analogWrite(R_PWM_right, spdFwd);
      analogWrite(R_PWM_left, spdFwd);
    }
    else if (ch1 < Ch1_start_Bac)
    {
      analogWrite(L_PWM_right, spdBac);
      analogWrite(L_PWM_left, spdBac);
    }

    // Handle right and left movement
    if (ch2 > Ch2_start_Right)
    {
      analogWrite(L_PWM_right, spdRight);
      analogWrite(R_PWM_left, spdRight);
    }
    else if (ch2 < Ch2_start_Left)
    {
      analogWrite(R_PWM_right, spdLeft);
      analogWrite(L_PWM_left, spdLeft);
    }
  }
}
