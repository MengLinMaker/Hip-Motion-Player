export default function resizeCanvas(camera, renderer, width, height) {
  const aspectRatio = width/height
  if (camera.aspect != aspectRatio) {
    camera.aspect = aspectRatio
    camera.updateProjectionMatrix()
    renderer.setSize( width, height )
  }
}