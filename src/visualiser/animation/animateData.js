import * as THREE from 'three'



// Animate the data
export default function animateData(hip, rightThigh, leftThigh, currentData, currentPosition){
  let q, qh, qr, ql

  qh = new THREE.Quaternion(currentData[7], currentData[8], currentData[9], currentData[6]).normalize()
  hip.rotation.setFromQuaternion(qh)
  qh = new THREE.Quaternion(currentData[7], currentData[8], currentData[9], -currentData[6]).normalize()

  hip.position.x = currentPosition[0]
  hip.position.y = currentPosition[1]
  hip.position.z = currentPosition[2]

  /*/
  const cosTh = currentData[6]**2 - currentData[9]**2
  const sinTh = 2 * currentData[6] * currentData[9]
  //let rotation = 360/Math.PI * Math.atan2(currentData[9],currentData[6])
  let rotation = 180/Math.PI * Math.atan2(sinTh,cosTh)
  rotation = (rotation+360) % 360
  //*/

  q = new THREE.Quaternion(currentData[17], currentData[18], currentData[19], currentData[16]).normalize()
  qr = new THREE.Quaternion().multiplyQuaternions(qh,q).normalize()
  rightThigh.rotation.setFromQuaternion(qr)

  q = new THREE.Quaternion(currentData[27], currentData[28], currentData[29], currentData[26]).normalize()
  ql = new THREE.Quaternion().multiplyQuaternions(qh,q).normalize()
  leftThigh.rotation.setFromQuaternion(ql)
}