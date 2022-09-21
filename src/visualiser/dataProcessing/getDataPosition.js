import * as THREE from 'three'

import relativePosition from './relativePosition'



const position = new relativePosition()

export default function getDataPosition(data) {
if (data != null) {
  let dataPosition=[]
  for (let timeStamp = 0; timeStamp < data.length; timeStamp++) {
    const currentData = data[timeStamp]
    const qh = new THREE.Quaternion(currentData[7], currentData[8], currentData[9], currentData[6]).normalize()
    const vector = new THREE.Vector3(currentData[3], currentData[4], currentData[5])
    vector.applyQuaternion(qh)
    vector.z = vector.z - 9.81
    dataPosition[timeStamp] = position.update([vector.x, vector.y, vector.z])
  }
  return dataPosition
}}