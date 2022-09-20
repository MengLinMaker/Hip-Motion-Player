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

Playing motion capture data from [Hip-Motion-Capture](https://github.com/MengLinMaker/Hip-Motion-Capture). The [captured motion data](https://github.com/MengLinMaker/Hip-Motion-Player/tree/main/Motion%20Data) is sampled at 50Hz. Each timestamp is represented by a row in the CSV file and displayed in the following format:

**Waist IMU data - Column A to J**
* Gyro (rad/s): x, y, z - Column A to C
* Acceleration (m/s^2): x, y, z - Column D to F
* Quaternion: w, x, y, z - Column G to J

**Right thigh IMU data - Column K to T**
* Gyro, Acceleration, Quaternion ... similar layout as above

**Right thigh IMU data - Column U to AD**
* Gyro, Acc, Quat ... similar layout as above



<div>&nbsp</div><div>&nbsp</div><div>&nbsp</div>

# How to use
1. Download the sample data from ['Motion Data'](https://github.com/MengLinMaker/Hip-Motion-Player/tree/main/Motion%20Data) folder.
2. Drag a CSV file onto the 3D model in the [demo website](https://menglinmaker-hip-motion-player.netlify.app/).
3. Press the pause/play button or drag the input slider.

Have fun!

<div>&nbsp</div><div>&nbsp</div><div>&nbsp</div>

# Developer instructions for integrating into other projects
1. Install dependencies in project root directory with `npm i localforage three`
2. Download the [src/visualiser](https://github.com/MengLinMaker/Hip-Motion-Player/tree/main/src/visualiser) folder.
3. In your project, create a div element: `<div id='visualiserID'/>`
4. At the start of a JavaScript file `import setupMotionVisualiser from './visualiser/visualiser.js'` tailored to your respective folder layout.
5. Evoke the function: `setupMotionVisualiser(document.querySelector('#visualiserID'), data, sampleRate)`
6. Input data should be formated as n by 30 array. Here is an [example data](https://github.com/MengLinMaker/Hip-Motion-Player/blob/main/src/sampleData.js).

Note: By default `data=null` and `sampleRate=50`. You can drag and drop CSV files
