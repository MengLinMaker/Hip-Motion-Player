import * as THREE from 'three'



export default function initialiseScene(scene, camera, renderer, sceneHeight) {
  scene.background = new THREE.Color( 0xffffff )
  camera.up.set( 0, 0, 1 )
  scene.position.set(0,0,sceneHeight)
  camera.position.set( 24, 12, 12 )

  renderer.setPixelRatio(window.devicePixelRatio)
  renderer.setSize(window.innerWidth, window.innerHeight)
  renderer.render(scene, camera)
  renderer.shadowMap.enabled = true
  renderer.shadowMap.type = THREE.PCFSoftShadowMap
  renderer.render(scene, camera)
}