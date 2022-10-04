import * as THREE from 'three'



export function quat2cosHeight(quat){
  // Project rotated axes to global z axis
  function quat2cosHeight2(q){
    q = new THREE.Quaternion(q[0], q[1], q[2], q[3]).normalize()
    const cosHeightX = new THREE.Vector3(1, 0, 0).applyQuaternion(q).z
    const cosHeightY = new THREE.Vector3(0, 1, 0).applyQuaternion(q).z
    const cosHeightZ = new THREE.Vector3(0, 0, 1).applyQuaternion(q).z
    return [cosHeightX, cosHeightY, cosHeightZ] 
  }

  if (Array.isArray(quat[0])){
    return quat.map((q) => {return quat2cosHeight2(q)})
  } else {
    return quat2cosHeight2(quat)
  }
}



export function poseFeature(data){
  function poseFeature2(d){
    let cosHeightArr = quat2cosHeight([d[7], d[8], d[9], d[6]])
    cosHeightArr = cosHeightArr.concat( quat2cosHeight([d[17], d[18], d[19], d[16]]) ) 
    cosHeightArr = cosHeightArr.concat( quat2cosHeight([d[27], d[28], d[29], d[26]]) )  
    return cosHeightArr
  }

  if (Array.isArray(data[0])){
    return data.map((d) => {return poseFeature2(d)})
  } else {
    return poseFeature2(data)
  }
}


function transpose(matrix) {
  let matrix2 = Array(matrix[0].length).fill(0)
  matrix2 = matrix2.map(()=>{ return Array(matrix.length) })
  for (let i = 0; i < matrix[0].length; i++) {
    for (let j = 0; j < matrix.length; j++) {
      matrix2[i][j] = matrix[j][i]
    }
  }
  return matrix2
}


function average(data) {
  function average2(d) {
    let sum = 0
    for (let i = 0; i < d.length; i++) { sum += d[i] }
    return sum/d.length
  }
  
  if (Array.isArray(data[0])){
    return data.map((d) => {
      return average2(d)})
  } else {
    return average2(data)
  }
}


function min(data) {
  function min2(d) {
    let least = 2**16
    for (let i = 0; i < d.length; i++) {
      if (least > d[i]) least = d[i]
    }
    return least
  }

  if (Array.isArray(data[0])){
    return data.map((d) => {
      return min2(d)})
  } else {
    return min2(data)
  }
}


function max(data) {
  function max2(d) {
    let most = -(2**16)
    for (let i = 0; i < d.length; i++) {
      if (most < d[i]) most = d[i]
    }
    return most
  }

  if (Array.isArray(data[0])){
    return data.map((d) => {
      return max2(d)})
  } else {
    return max2(data)
  }
}


export function motionFeature(data, subSample=1){
  //const dataHigh = butterIIR(data.T, 1, sampleRate/subSample, 2).T
  //waistAccNorm = norm(dataHigh[:, 3:6])
  //rightAccNorm = norm(dataHigh[:, 13:16])
  //leftAccNorm = norm(dataHigh[:, 23:26])
  //aveAccNorm = np.array([np.average(waistAccNorm), np.average(rightAccNorm), np.average(leftAccNorm)])
  //aveAccEnergy = np.array([np.average(waistAccNorm**2), np.average(rightAccNorm**2), np.average(leftAccNorm**2)])

  const orientationFeature = poseFeature(data)
  const aveOrientationFeature = average(transpose(orientationFeature))
  const minOrientationFeature = min(transpose(orientationFeature))
  //waistGyro = data[0:3, :]
  //rightGyro = data[10:13, :]
  //leftGyro = data[20:23, :]
  //gyro = np.r_[ waistGyro, rightGyro, leftGyro]

  //gyroNorm = np.r_[norm(waistGyro), norm(rightGyro), norm(leftGyro)]
  //waistAcc = data[:, [3, 4, 5]]
  //rightAcc = data[:, [13, 14, 15]]
  //leftAcc = data[:, [23, 24, 25]]

  let feature = orientationFeature[0]
  feature = feature.concat(orientationFeature[orientationFeature.length-1])
  feature = feature.concat(aveOrientationFeature)
  //feature = feature.concat(np.max(orientationFeature, axis=0))
  feature = feature.concat(minOrientationFeature)
  //aveAccNorm,
  //np.average(gyro, axis=0),
  //np.sum(aveAccEnergy),
  //np.average(gyroNorm, axis=0),
  return feature
}