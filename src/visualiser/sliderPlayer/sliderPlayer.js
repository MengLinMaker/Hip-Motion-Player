import { playIcon, pausedIcon } from '../asset'
import './sliderPlayer.css'



export default class SliderPlayer {
  #scrubber
  #scrubberLabel
  #playButtonIcon

  #scrubberCounter = 0
  #myValuePlayer = null
  #playing = false
  #dataRate



  constructor(sliderPlayer, dataRate){
    sliderPlayer.innerHTML = `
    <button id='playButton' name='playButton' style='border: none; background-color: inherit; border-radius: 50%; height: 2rem; width: 2rem; display: flex; align-items: center; justify-content: center; margin-right: 0.5rem;'
      onMouseOver="this.style.backgroundColor='#eeeeee'"
      onMouseOut="this.style.backgroundColor='inherit'"
    >
      <img alt='playButtonIcon' id="playButtonIcon" style='height: 1.2rem; width: 1.2rem; user-select: none;'/>
    </button>
    <label id='scrubberLabel' for='scrubber' style='font-size: 0.8rem; font-family: Arial;'>0.00s</label>
    <input style="flex-grow: 1; margin-left: 1rem; margin-right: 1rem; height: 3.2px; accent-color: #111111;"
    type="range" id="scrubber" name="scrubber" min="0" max="0">`



    this.#dataRate = dataRate

    this.#scrubber = document.querySelector('#scrubber')
    this.#scrubberLabel = document.querySelector('#scrubberLabel')
    this.#playButtonIcon = document.querySelector('#playButtonIcon')

    this.#scrubber.max = 0
    this.#playButtonIcon.src = playIcon

    // Update scrubber on input change
    this.#scrubber.addEventListener('input', (e)=>{
      this.updateScrubber( parseFloat(scrubber.value), this.#dataRate)
    })

    const playButton = document.querySelector('#playButton')
    playButton.addEventListener('click', ()=>{this.playButtonHandler()})
  }



  updateScrubber(value) {
    this.#scrubber.value = value
    this.#scrubberCounter = value
    this.#scrubberLabel.innerText = (value/this.#dataRate).toFixed(2) + 's'
  }

  // Play/pause button handler
  playButtonHandler() {
    if (this.#playing == true) {
      this.#playButtonIcon.src = playIcon
      this.#playing = false
      clearInterval(this.#myValuePlayer)
    } else if (this.#scrubber.max != 0) {
      this.#playButtonIcon.src = pausedIcon
      this.#playing = true
      this.#myValuePlayer = setInterval(()=>{
        this.updateScrubber(this.#scrubberCounter)
        if (this.#scrubberCounter < this.#scrubber.max) this.#scrubberCounter += 1
        else this.#scrubberCounter = 0
      }, 1000/this.#dataRate)
    }
  }

  getScrubberCounter() { return this.#scrubberCounter }

  isPlaying() { return this.#playing }

  setDataRate(dataRate) { this.#dataRate = dataRate }

  setScrubberMax(scrubberMax) {this.#scrubber.max = scrubberMax}
}