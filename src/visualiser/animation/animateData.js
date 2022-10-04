import * as THREE from 'three'


let mirror = 1
// Animate the data
export default function animateData(hip, rightThigh, leftThigh, currentData, currentPosition){
  let q, qh, qr, ql
  //mirror = -mirror

  qh = new THREE.Quaternion(mirror*currentData[7], currentData[8], mirror*currentData[9], currentData[6]).normalize()
  hip.rotation.setFromQuaternion(qh)
  qh = new THREE.Quaternion(mirror*currentData[7], currentData[8], mirror*currentData[9], -currentData[6]).normalize()

  hip.position.x = currentPosition[0]
  hip.position.y = mirror*currentPosition[1]
  hip.position.z = currentPosition[2]

  /*/
  const cosTh = currentData[6]**2 - currentData[9]**2
  const sinTh = 2 * currentData[6] * currentData[9]
  //let rotation = 360/Math.PI * Math.atan2(currentData[9],currentData[6])
  let rotation = 180/Math.PI * Math.atan2(sinTh,cosTh)
  rotation = (rotation+360) % 360
  //*/

  q = new THREE.Quaternion(mirror*currentData[17], currentData[18], mirror*currentData[19], currentData[16]).normalize()
  qr = new THREE.Quaternion().multiplyQuaternions(qh,q).normalize()
  if (mirror == 1) rightThigh.rotation.setFromQuaternion(qr)
  else leftThigh.rotation.setFromQuaternion(qr)

  q = new THREE.Quaternion(mirror*currentData[27], currentData[28], mirror*currentData[29], currentData[26]).normalize()
  ql = new THREE.Quaternion().multiplyQuaternions(qh,q).normalize()
  if (mirror == 1) leftThigh.rotation.setFromQuaternion(ql)
  else rightThigh.rotation.setFromQuaternion(ql)

}