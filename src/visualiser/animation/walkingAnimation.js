import * as THREE from 'three'



// Making a walking animation
let counter = 0
export default function walkingAnimation(hip, rightThigh, leftThigh, FPS){
  const interval = 1/FPS
  const speed = 1.1
  counter += Math.PI*interval*speed
  const sc = Math.sin(counter)

  hip.rotation.z += Math.PI/4*interval*Math.sqrt(speed)
  hip.rotation.x = 0.08*sc
  hip.position.z = 0.2*sc

  let q = new THREE.Quaternion(0.05,0.18,0,sc-0.2)
  leftThigh.rotation.setFromQuaternion(q)
  q = new THREE.Quaternion(0.05,0.18,0,-sc-0.2)
  rightThigh.rotation.setFromQuaternion(q)
}