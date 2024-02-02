/**
  This add-on replaces the plain text editor with an advanced code editor.
  This is an implementation of Mini Code Editor to More Points
  https://github.com/AdrBog/MiniCodeEditor
**/

import { MiniCodeEditor } from "./editor.js"
import { RULES } from "./rules.js"

window.RULES = RULES

window.addEventListener("load", () => {
  const oldTextarea = document.querySelector("textarea")
  const value = oldTextarea.value
  oldTextarea.remove()
  document.querySelector(".text-editor").insertAdjacentHTML("beforeend", "<div id='text-editor'></div><div id='text-editor-toolbar' class='toolbar'></div>")
  window.CODE_EDITOR = new MiniCodeEditor("#text-editor", "content")
  window.CODE_EDITOR.setFontSize(24)
  window.CODE_EDITOR.setValue(value)
  generateToolbar(document.querySelector("#text-editor-toolbar"))
})

function generateToolbar(toolbar){
  const RULES_OPTIONS = Object.keys(RULES).map((x) => {return `<option value='${x}'>${x}</option>`}).join("")
  toolbar.innerHTML = `
    <div>
      <label for="word-wrap">Word Wrap:</label>
      <input type="checkbox" name="word-wrap" id="word-wrap" onchange="window.CODE_EDITOR.setWordWrap(this.checked)">
    </div>
    <button type="button" onclick="window.CODE_EDITOR.setFontSize(window.CODE_EDITOR.fontSize + 2)">Font +</button>
    <button type="button" onclick="window.CODE_EDITOR.setFontSize(window.CODE_EDITOR.fontSize - 2)">Font -</button>
    <select id="text-editor-rule" onchange="window.CODE_EDITOR.setRules(window.RULES[this.value])">
      ${RULES_OPTIONS}
    </select>
  `
  const SELECT = document.querySelector("#text-editor-rule")
  switch(document.querySelector("[name='filename']").value.split(".").slice(-1)[0]){
    case "css":
      SELECT.value = "css"
      break;
    case "svg":
    case "xml":
    case "html":
      SELECT.value = "html"
      break;
    case "js":
      SELECT.value = "js"
      break;
    case "py":
      SELECT.value = "python"
      break;
    case "sql":
      SELECT.value = "sqlite"
      break;
    default:
      SELECT.value = "plain-text"
  }
  window.CODE_EDITOR.setRules(window.RULES[SELECT.value])
}
