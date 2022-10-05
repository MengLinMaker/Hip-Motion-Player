import * as THREE from 'three'
import Fili from 'fili'
import { clf } from './SVC'



function arrayHandler(arr, func) {
  if (Array.isArray(arr[0])){
    return arr.map((q) => {return func(q)})
  } else {
    return func(arr)
  }
}



export function quat2cosHeight(quat){
  // Project rotated axes to global z axis
  function quat2cosHeight2(q){
    q = new THREE.Quaternion(q[0], q[1], q[2], q[3]).normalize()
    const cosHeightX = new THREE.Vector3(1, 0, 0).applyQuaternion(q).z
    const cosHeightY = new THREE.Vector3(0, 1, 0).applyQuaternion(q).z
    const cosHeightZ = new THREE.Vector3(0, 0, 1).applyQuaternion(q).z
    return [cosHeightX, cosHeightY, cosHeightZ] 
  }
  return arrayHandler(quat, quat2cosHeight2)
}



export function poseFeature(data){
  function poseFeature2(d){
    let cosHeightArr = quat2cosHeight([d[7], d[8], d[9], d[6]])
    cosHeightArr = cosHeightArr.concat( quat2cosHeight([d[17], d[18], d[19], d[16]]) ) 
    cosHeightArr = cosHeightArr.concat( quat2cosHeight([d[27], d[28], d[29], d[26]]) )  
    return cosHeightArr
  }
  return arrayHandler(data, poseFeature2)
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
  return arrayHandler(data, average2)
}



function min(data) {
  function min2(d) {
    let least = 2**16
    for (let i = 0; i < d.length; i++) {
      if (least > d[i]) least = d[i]
    }
    return least
  }
  return arrayHandler(data, min2)
}



function max(data) {
  function max2(d) {
    let most = -(2**16)
    for (let i = 0; i < d.length; i++) {
      if (most < d[i]) most = d[i]
    }
    return most
  }
  return arrayHandler(data, max2)
}



function norm(data) {
  function norm2(d) {
    let val = 0
    for (let i = 0; i < d.length; i++) {
      val += d[i]**2
    }
    return val**0.5
  }
  return arrayHandler(data, norm2)
}



const iirCalculator = new Fili.CalcCascades();
function highPassFilter(data, Fs, Fc) {
  const iirHighPass = iirCalculator.highpass({ order: 1, characteristic: 'butterworth', Fs: Fs, Fc: Fc })
  const iirFilter = new Fili.IirFilter(iirHighPass)

  function highPassFilter2(d) {
    return iirFilter.simulate(d)
  }
  return arrayHandler(data, highPassFilter2)
}



export function motionFeature(data, sampleRate){
  const windowSec = 3
  if (data.length > windowSec*sampleRate) {
    data = data.slice(0,windowSec*sampleRate)
  }

  const orientationFeature = poseFeature(data)
  const orientationFeatureT = transpose(orientationFeature)
  
  const waistAccHigh = highPassFilter(transpose(data).slice(3, 6), sampleRate, 1)
  const rightAccHigh = highPassFilter(transpose(data).slice(13, 16), sampleRate, 1)
  const leftAccHigh = highPassFilter(transpose(data).slice(23, 26), sampleRate, 1)
  
  const waistAccNorm = norm(transpose(waistAccHigh))
  const rightAccNorm = norm(transpose(rightAccHigh))
  const leftAccNorm = norm(transpose(leftAccHigh))

  const aveAccNorm = [average(waistAccNorm), average(rightAccNorm), average(leftAccNorm)]

  let feature = orientationFeature[0]
  feature = feature.concat(orientationFeature[orientationFeature.length-1])
  feature = feature.concat(average(orientationFeatureT))
  //feature = feature.concat(np.max(orientationFeature, axis=0))
  feature = feature.concat(min(orientationFeatureT))
  feature = feature.concat(aveAccNorm)
  return feature
}


let oldClassID = -1
let filterClassID = -1
let counter = 0
export function classifyMotion(data, sampleRate) {
  const feature = motionFeature(data, sampleRate)
  const classID = clf.predict(feature)

  if (oldClassID == -1) {
    oldClassID = classID
    filterClassID = classID
    counter = 0
  } else if (classID == oldClassID) {
    counter += 1
    if (counter > 50) filterClassID = classID
  } else counter = 0
  oldClassID = classID

  const className = ['Fall Back', 'Fall Front', 'Fall Left', 'Fall Right', 'Jump', 'Run', 'Sit', 'Stair', 'Stand', 'Walk']
  return className[filterClassID]
}