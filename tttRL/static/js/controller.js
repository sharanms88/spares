function myFunction() {
	let n1 = Math.random()
	var responseElement = document.getElementById("resonse")
	if(!responseElement){
		var responseElement = document.createElement("p");
		responseElement.id = "resonse"
		document.body.appendChild(responseElement);
	} 
	responseElement.innerHTML = Math.random();

}