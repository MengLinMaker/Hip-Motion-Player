import './style.css'
import setupMotionVisualiser from './visualiser/visualiser.js'

document.querySelector('#app').innerHTML = `
  <div style='position: absolute; width: 100%; z-index: 10; bottom: 0.5rem; text-align: center'>
    <p style='font-family: Verdana; font-size: 0.8rem;'>Drag & Drop motion data to play</p>
  </div>
  <div id="visualiserContainer"\>
`

setupMotionVisualiser(document.querySelector('#visualiserContainer'))