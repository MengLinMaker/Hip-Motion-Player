<h1 align="center"> Hip Motion Capture - <a href="https://menglinmaker-hip-motion-player.netlify.app/">Demo</a></h1>

<div align="center">
  <img width="500" src="https://user-images.githubusercontent.com/39476147/189935030-371cc4b4-a2a7-4ff3-9d71-7a1369c090a9.gif"
  href="https://menglinmaker-hip-motion-player.netlify.app/"/>
</div>

<div flex align="center">
  <img alt="GitHub" src="https://img.shields.io/github/license/menglinmaker/Hip-Motion-Player?style=flat-square">
  <img src="https://img.shields.io/github/languages/code-size/menglinmaker/Hip-Motion-Player?style=flat-square">
  <img src="https://img.shields.io/website?down_color=red&down_message=offline&up_color=success&up_message=online&url=https://menglinmaker-hip-motion-player.netlify.app/&style=flat-square">
</div>

Playing motion capture data from [Hip-Motion-Capture](https://github.com/MengLinMaker/Hip-Motion-Capture). The [captured motion data](https://github.com/MengLinMaker/Hip-Motion-Player/tree/main/Motion%20Data) is sampled at 50Hz. Each time stamp is represented by a row in the csv fle and layed out in the following format:

**Waist IMU data: Column A to J**
* Gyro (rad/s): x, y, z
* Acceleration (m/s^2): x, y, z
* Quaternion: w, x, y, z

**Right thigh IMU data: Column K to T**
* Gyro, Acc, Quaternion ... same layout as above

**Right thigh IMU data: Column U to AD**
* Gyro, Acc, Quaternion ... same layout as above
