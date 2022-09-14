import * as THREE from 'three'



export default function setupScene(scene, sceneHeight) {
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
}