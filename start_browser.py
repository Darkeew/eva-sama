from selenium import webdriver
import pyautogui
import time

def start(browser):
    time.sleep(3)
    pyautogui.click(900,0)
    pyautogui.press('f')
    pyautogui.click(1862, 1054)
    time.sleep(0.2)
    pyautogui.click(1716, 833)
    time.sleep(0.2)
    pyautogui.click(1599, 888)
    time.sleep(0.2)
    pyautogui.click(918, 800)
    browser.execute_script("""
const liveTime = document.querySelector(".live-time");

const style = document.createElement("style");
style.id = "on-video-time-style";
style.textContent = `#on-video-time {
  position: absolute;
  padding: .5rem;
  top: 0;
  right: .3rem;
  z-index: 9999;

  color: black;
  font-size: 9rem;
  font-weight: bold;
  text-shadow: 0 0 4px white;
}`;

document.head.appendChild(style);

const onVideoTime = document.createElement("div");
onVideoTime.id = "on-video-time";
onVideoTime.textContent = liveTime.textContent;

const videoContainer = document.querySelector(".video-ref");
videoContainer.insertBefore(onVideoTime, videoContainer.children[0])

const observer = new MutationObserver((mutations) => {
  for (const mutation of mutations) {
    if (mutation.type === "characterData") {
      onVideoTime.textContent = mutation.target.textContent
    }
  }
});

observer.observe(liveTime, {
  characterData: true,
  subtree: true
});
""")
