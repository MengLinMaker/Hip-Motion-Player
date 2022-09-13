import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader'

import relativePosition from './relativePosition'
import csvToArray from './csvToArray'

import hipSTL from '../asset/hip.stl?url'
import rightThighSTL from '../asset/rightThigh.stl?url'
import leftThighSTL from '../asset/leftThigh.stl?url'

import playIcon from '../asset/icons8-play-96.png?url'
import pausedIcon from '../asset/icons8-pause-96.png?url'



export default function setupMotionVisualiser(visualiserContainer) {
let data = null
let scrubberCounter = 0

visualiserContainer.innerHTML=`
  <div style='position: relative; display: flex; flex-direction: column; align-items: center; justify-content: center; overflow: hidden;'>
    <canvas id="visualiser" style='width: 100%;'></canvas>
    <div id='player' style='position: absolute; background-color: #ffffffdd; backdrop-filter: blur(3px); bottom: 3rem; padding: 0.3rem; width: 80%; display: flex; align-items: center; border-radius: 10rem; box-shadow: 0 1px 3px #00000044;'>
      <button style='border: none; background-color: inherit; border-radius: 50%; height: 2rem; width: 2rem; display: flex; align-items: center; justify-content: center;'
        onMouseOver="this.style.backgroundColor='#eeeeee'"
        onMouseOut="this.style.backgroundColor='inherit'"
      >
        <img id="playButton" style='height: 1.2rem; width: 1.2rem;'/>
      </button>
      <input style="flex-grow: 1; margin-left: 0.5rem; margin-right: 1rem; height: 3.2px; accent-color: #111111;"
      type="range" id="scrubber" name="scrubber" min="0" max="0">
    </div>
  </div>
`
const scrubber = document.querySelector('#scrubber')
const visualiserElement = document.querySelector('#visualiser')
visualiserElement.addEventListener('dragover', (e)=>{e.preventDefault()})

visualiserElement.addEventListener('drop', (e)=>{
  e.preventDefault()
  e.stopPropagation()
  if (e.dataTransfer.files.length) {
    const file = e.dataTransfer.files[0]
    if (file.name.slice(-3) == 'csv') {
      const reader = new FileReader()
      reader.readAsText(file)
      reader.onload = (e)=>{
        const text = e.target.result
        data = csvToArray(text)
        scrubber.max = data.length - 1
        window.currentData = data[0]
        scrubberCounter = 0
        playButtonHandler()
      }
    }
  }
})

const playButton = document.querySelector('#playButton')
let playing = false
playButton.src = playIcon
function playButtonHandler() {
  if (playing) {
    playButton.src = playIcon
    playing = false
    console.log('playIcon')
  } else if (data != null) {
    playButton.src = pausedIcon
    playing = true
    console.log('pausedIcon')
  }
}
playButton.addEventListener('click', playButtonHandler)

scrubber.addEventListener('input', (e)=>{
  scrubberCounter = scrubber.value
  console.log(scrubberCounter)
})

setInterval(()=>{
  if (data != null && playing == true) {
    window.currentData = data[scrubberCounter]
    scrubber.value = scrubberCounter
    if (scrubberCounter <= scrubber.max) scrubberCounter += 1
    else scrubberCounter = 0
  }
}, 1000/50)





const sceneHeight = 2.8

// Setting up three js canvas
const scene = new THREE.Scene()
scene.background = new THREE.Color( 0xffffff )

const camera = new THREE.PerspectiveCamera(30, window.innerWidth/window.innerHeight, 0.1, 1000)
camera.up.set( 0, 0, 1 )
scene.position.set(0,0,sceneHeight)
camera.position.set( 24, 12, 12 )

const renderer = new THREE.WebGLRenderer({
  canvas: visualiserElement,
})
renderer.setPixelRatio(window.devicePixelRatio)
renderer.setSize(window.innerWidth, window.innerHeight)
renderer.render(scene, camera)
renderer.shadowMap.enabled = true
renderer.shadowMap.type = THREE.PCFSoftShadowMap
renderer.render(scene, camera)

// Importing orbit controls
const controls = new OrbitControls(camera, renderer.domElement)

// Window resize functionality
function resizeCanvas() {
  const aspectRatio = visualiserContainer.clientWidth/ visualiserContainer.clientHeight
  if (camera.aspect != aspectRatio) {
    camera.aspect = aspectRatio
    camera.updateProjectionMatrix()
    renderer.setSize( visualiserContainer.clientWidth, visualiserContainer.clientHeight )
  }
}






// Ground plane
//*/
const plane = new THREE.Mesh(
    new THREE.PlaneGeometry( 400, 400 ),
    new THREE.MeshPhysicalMaterial( { color: 0xfffffff } )
)
plane.translateZ(-10)
scene.add( plane )
plane.receiveShadow = true
//*/





const loader = new STLLoader()
const material = new THREE.MeshPhysicalMaterial( { color: 0xaa8866, clearcoat: 0.8, roughness: 0.5, clearcoatRoughness: 0.5 } )

let hip
loader.load(
  hipSTL,
  function (geometry) {
    const mesh = new THREE.Mesh( geometry, material )
    mesh.castShadow = true
    mesh.receiveShadow = true

    mesh.scale.set( 10, 10, 10 )
    hip = mesh
    scene.add(mesh)

    loadRightThigh()
    loadLeftThigh()
  }
)

let rightThigh
function loadRightThigh(){
  loader.load(
    rightThighSTL,
    function (geometry) {
      const mesh = new THREE.Mesh( geometry, material )
      mesh.castShadow = true
      mesh.receiveShadow = true

      mesh.position.set( 0, -0.086, -0.019 )
      rightThigh = mesh
      hip.add(rightThigh)
    }
  )
}

let leftThigh
function loadLeftThigh(){
  loader.load(
    leftThighSTL,
    function (geometry) {
      const mesh = new THREE.Mesh( geometry, material )
      mesh.castShadow = true
      mesh.receiveShadow = true

      mesh.position.set( 0, 0.086, -0.019 )
      leftThigh = mesh
      hip.add(leftThigh)
    }
  )
}








// Defining lights
scene.add( new THREE.HemisphereLight( 0x443333, 0x111122 ) )
addShadowedLight( 10, 10, 50 + sceneHeight, 0xffffff, 2.5 )
addShadowedLight( 50, 0, - 50 + sceneHeight, 0xffccaa, 3 )
addShadowedLight( -10, -5, -10 + sceneHeight, 0xccaa88, 3 )
function addShadowedLight( x, y, z, color, intensity ) {
  const directionalLight = new THREE.DirectionalLight( color, intensity )
  directionalLight.position.set( x, y, z )
  scene.add( directionalLight )
  directionalLight.castShadow = true
  const side = 15
  directionalLight.shadow.camera.top = side
  directionalLight.shadow.camera.bottom = -side
  directionalLight.shadow.camera.left = side
  directionalLight.shadow.camera.right = -side
  directionalLight.shadow.mapSize.width = 2**10
  directionalLight.shadow.mapSize.height = 2**10
}








// Rendering and animate at set fps
const clock = new THREE.Clock()
let delta = 0
const interval = 1 / 60
function animate() {
  resizeCanvas()
  requestAnimationFrame(animate)
  delta += clock.getDelta()
  if (delta  > interval) {

    if (hip != null && rightThigh != null && leftThigh != null){
      if (window.currentData != null) animateData()
      else walkingAnimation()
      controls.update()
      renderer.render(scene, camera)
      delta = delta % interval
    }

  }
}
animate()





// Animate the data
let q, qh, qr, ql
const position = new relativePosition()
function animateData(){
  const data = window.currentData

  qh = new THREE.Quaternion(data[7], data[8], data[9], data[6]).normalize()
  const vector = new THREE.Vector3(data[3], data[4], data[5])
  vector.applyQuaternion(qh)
  hip.rotation.setFromQuaternion(qh)
  qh = new THREE.Quaternion(data[7], data[8], data[9], -data[6]).normalize()

  vector.z = vector.z - 9.81
  const pos = position.update([vector.x, vector.y, vector.z])
  hip.position.x = pos[0]
  hip.position.y = pos[1]
  hip.position.z = pos[2] 

  const cosTh = data[6]**2 - data[9]**2
  const sinTh = 2 * data[6] * data[9]
  //let rotation = 360/Math.PI * Math.atan2(data[9],data[6])
  let rotation = 180/Math.PI * Math.atan2(sinTh,cosTh)
  rotation = (rotation+360) % 360

  q = new THREE.Quaternion(data[17], data[18], data[19], data[16]).normalize()
  qr = new THREE.Quaternion().multiplyQuaternions(qh,q).normalize()
  rightThigh.rotation.setFromQuaternion(qr)

  q = new THREE.Quaternion(data[27], data[28], data[29], data[26]).normalize()
  ql = new THREE.Quaternion().multiplyQuaternions(qh,q).normalize()
  leftThigh.rotation.setFromQuaternion(ql)
}






// Making a walking animation
let counter = 0
const speed = 1.1
function walkingAnimation(){
  counter += Math.PI*interval*speed
  const sc = Math.sin(counter)

  hip.rotation.z += Math.PI/4*interval*Math.sqrt(speed)
  hip.rotation.x = 0.08*sc
  hip.position.z = 0.2*sc

  q = new THREE.Quaternion(0.05,0.18,0,sc-0.2)
  leftThigh.rotation.setFromQuaternion(q)
  q = new THREE.Quaternion(0.05,0.18,0,-sc-0.2)
  rightThigh.rotation.setFromQuaternion(q)
}


}