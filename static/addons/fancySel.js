/**
	This add-on facilitates file selection.
	It allows the selection of multiple files by holding down the CTRL key.
**/

var table = document.querySelector(".files-list");

table.addEventListener("click", (e) => {
	if (Array.from(e.target.classList).includes("file")){
		let checkbox = e.target.parentElement.querySelector("[type='checkbox']");
		if (!e.ctrlKey) {
			Array.from(table.querySelectorAll("[type='checkbox']")).map((x) => {x.checked = false})
		}
		checkbox.checked = ! checkbox.checked;
		updateSelected()
	}
})
