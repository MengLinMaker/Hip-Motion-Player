import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader'

import { hipSTL, rightThighSTL, leftThighSTL } from './asset'

import { csvToArray, getCachedBlobUrl, getDataPosition } from './dataProcessing'
import { initialiseScene, resizeCanvas, setupScene } from './scene'
import { animateData, walkingAnimation } from './animation'
import SliderPlayer from './sliderPlayer/sliderPlayer'



export default async function setupMotionVisualiser(visualiserContainer, data=null, dataRate=50, FPS=60) {

// HTML content
visualiserContainer.innerHTML=`
<div style='position: relative; display: flex; flex-direction: column; align-items: center; justify-content: center; overflow: hidden;'>
  <canvas id="visualiser" style='width: 100%;'></canvas>
  <div id='sliderPlayer' style='position: absolute; background-color: #ffffffdd; backdrop-filter: blur(3px); bottom: 3rem; padding: 0.3rem; width: 80%; display: flex; align-items: center; border-radius: 10rem; box-shadow: 0 1px 3px #00000044; max-width: 600px;'></div>
</div>`

// create a slider player for data control
const sliderPlayer = new SliderPlayer(document.querySelector('#sliderPlayer'), dataRate)
const visualiserElement = document.querySelector('#visualiser')

let dataPosition = getDataPosition(data)

// Prepare initialised data
if (data != null) {
  sliderPlayer.setScrubberMax(data.length-1)
  sliderPlayer.playButtonHandler()
}

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
        dataPosition = getDataPosition(data)

        sliderPlayer.setScrubberMax(data.length - 1)
        sliderPlayer.updateScrubber(0)
        if (sliderPlayer.isPlaying() == false) sliderPlayer.playButtonHandler()

      }
    }
  }
})






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





// Loading 3D model 
let hip, hipSTLurl
let rightThigh, rightThighSTLurl
let leftThigh, leftThighSTLurl

hipSTLurl = await getCachedBlobUrl(hipSTL, 'hipSTL')
rightThighSTLurl = await getCachedBlobUrl(rightThighSTL, 'rightThighSTL')
leftThighSTLurl = await getCachedBlobUrl(leftThighSTL, 'leftThighSTL')

const loader = new STLLoader()
const material = new THREE.MeshPhysicalMaterial( { color: 0xaa8866, clearcoat: 0.8, roughness: 0.5, clearcoatRoughness: 0.5 } )

loader.load(
  hipSTLurl,
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
    rightThighSTLurl,
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
    leftThighSTLurl,
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
      if (data != null) {
        const scrubberCounter = sliderPlayer.getScrubberCounter()
        animateData(hip, rightThigh, leftThigh, data[scrubberCounter], dataPosition[scrubberCounter])
      }
      else walkingAnimation(hip, rightThigh, leftThigh, FPS)
      controls.update()
    }

    renderer.render(scene, camera)
    delta = delta % interval
  }
}
animate()


}