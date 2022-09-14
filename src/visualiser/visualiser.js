import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader'

import { hipSTL, rightThighSTL, leftThighSTL, playIcon, pausedIcon } from './asset'

import { csvToArray, getDataPosition } from './dataProcessing'
import { initialiseScene, resizeCanvas, setupScene } from './scene'
import { animateData, walkingAnimation } from './animation'



export default function setupMotionVisualiser(visualiserContainer, data=null, dataRate=50, FPS=60) {

// HTML content
visualiserContainer.innerHTML=`
<div style='position: relative; display: flex; flex-direction: column; align-items: center; justify-content: center; overflow: hidden;'>
  <canvas id="visualiser" style='width: 100%;'></canvas>
  <div id='player' style='position: absolute; background-color: #ffffffdd; backdrop-filter: blur(3px); bottom: 3rem; padding: 0.3rem; width: 80%; display: flex; align-items: center; border-radius: 10rem; box-shadow: 0 1px 3px #00000044; max-width: 600px;'>
    <button id='playButton' name='playButton' style='border: none; background-color: inherit; border-radius: 50%; height: 2rem; width: 2rem; display: flex; align-items: center; justify-content: center; margin-right: 0.5rem'
      onMouseOver="this.style.backgroundColor='#eeeeee'"
      onMouseOut="this.style.backgroundColor='inherit'"
    >
      <img alt='playButtonIcon' id="playButtonIcon" style='height: 1.2rem; width: 1.2rem; user-select: none;'/>
    </button>
    <label id='scrubberLabel' for='scrubber' style='font-size: 0.75rem; font-family: Monaco;'>0.00s</label>
    <input style="flex-grow: 1; margin-left: 1rem; margin-right: 1rem; height: 3.2px; accent-color: #111111;"
    type="range" id="scrubber" name="scrubber" min="0" max="0">
  </div>
</div>`



let scrubberCounter = 0
let myValuePlayer = null
let dataPosition = getDataPosition(data)

const scrubber = document.querySelector('#scrubber')
const scrubberLabel = document.querySelector('#scrubberLabel')
const visualiserElement = document.querySelector('#visualiser')
const playButton = document.querySelector('#playButton')
const playButtonIcon = document.querySelector('#playButtonIcon')

function updateScrubber(value, dataRate) {
  scrubber.value = value
  scrubberCounter = value
  scrubberLabel.innerText = (value/dataRate).toFixed(2) + 's'
}

// Update scrubber on input change
scrubber.addEventListener('input', (e)=>{
  updateScrubber( parseFloat(scrubber.value), dataRate)
})

// Drag and drop file event listeners
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
        dataPosition = getDataPosition(data)
        updateScrubber(0, dataRate)
        if (playing == false) playButtonHandler()

      }
    }
  }
})


// Play/pause button handler
let playing = false
playButtonIcon.src = playIcon
function playButtonHandler() {
  if (playing) {
    playButtonIcon.src = playIcon
    playing = false
    clearInterval(myValuePlayer)
  } else if (data != null) {
    playButtonIcon.src = pausedIcon
    playing = true
    myValuePlayer = setInterval(()=>{
      updateScrubber(scrubberCounter,dataRate)
      if (scrubberCounter < scrubber.max) scrubberCounter += 1
      else scrubberCounter = 0
    }, 1000/dataRate)
  }
}
playButton.addEventListener('click', playButtonHandler)

// Prepare initialised data
if (data != null) {
  scrubber.max = data.length-1
  playButtonHandler()
}





// Initialising 3D visulisation
const sceneHeight = 2.8

// Setting up three js canvas
const scene = new THREE.Scene()
const camera = new THREE.PerspectiveCamera(30, window.innerWidth/window.innerHeight, 0.1, 1000)
const renderer = new THREE.WebGLRenderer({
  canvas: visualiserElement,
})
const controls = new OrbitControls(camera, renderer.domElement) // Importing orbit controls

initialiseScene(scene, camera, renderer, sceneHeight)
setupScene(scene, sceneHeight)





// Loading the 3D model 
let hip
let rightThigh
let leftThigh
const loader = new STLLoader()
const material = new THREE.MeshPhysicalMaterial( { color: 0xaa8866, clearcoat: 0.8, roughness: 0.5, clearcoatRoughness: 0.5 } )

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





// Rendering and animate at set fps
const clock = new THREE.Clock()
let delta = 0
const interval = 1 / FPS
function animate() {
  resizeCanvas(camera, renderer, visualiserContainer.clientWidth, visualiserContainer.clientHeight)
  requestAnimationFrame(animate)
  delta += clock.getDelta()
  if (delta > interval) {

    if (hip != null && rightThigh != null && leftThigh != null){
      if (data != null) animateData(hip, rightThigh, leftThigh, data[scrubberCounter], dataPosition[scrubberCounter])
      else walkingAnimation(hip, rightThigh, leftThigh)
      controls.update()
    }

    renderer.render(scene, camera)
    delta = delta % interval
  }
}
animate()


}