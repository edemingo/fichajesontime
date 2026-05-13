



async function getFicheros() {

    clearAllResults()
    const resp = await fetch(`/api/ficheros`);
    const data = await resp.json();

    const resultsEl = document.getElementById("resultsFiles");


    resultsEl.innerHTML = data.map(r => {
    return `
      <div class="row m-1 p-1 align-items-start border">
        <div class='col-6 fw-bold'>${r.nombre_fichero}</div>       
        <div class='col-3 text-end'>
        
            <button class='btn btn-outline-primary' onclick='verFicheroGet("${r.nombre_fichero}")' data-fichero='${r.nombre_fichero}'>
            <svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' class='bi bi-body-text' viewBox='0 0 16 16'>
                <path fill-rule='evenodd' d='M0 .5A.5.5 0 0 1 .5 0h4a.5.5 0 0 1 0 1h-4A.5.5 0 0 1 0 .5m0 2A.5.5 0 0 1 .5 2h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5m9 0a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5m-9 2A.5.5 0 0 1 .5 4h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5m5 0a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5m7 0a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5m-12 2A.5.5 0 0 1 .5 6h6a.5.5 0 0 1 0 1h-6a.5.5 0 0 1-.5-.5m8 0a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5m-8 2A.5.5 0 0 1 .5 8h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5m7 0a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5m-7 2a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 0 1h-8a.5.5 0 0 1-.5-.5m0 2a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 0 1h-4a.5.5 0 0 1-.5-.5m0 2a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 0 1h-2a.5.5 0 0 1-.5-.5'/>
            </svg> Visualizar Fichero</button>
        
        </div>        

        <div class='col-3 text-end'>
        
            <button class='btn btn-outline-danger' onclick='procesarFicheroGet("${r.nombre_fichero}")' data-fichero='${r.nombre_fichero}'> 
                <svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' class='bi bi-plus' viewBox='0 0 16 16'>
                    <path d='M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4'/>
                </svg> Importar Fichero
            </button>

        </div>        
      </div>
    `;
  })
  .join("");
};





const verFicheroGet = async function(theFile){
    const resp = await fetch(`/api/verFichero?nombre_fichero=${encodeURIComponent(theFile)}`);
    const data = await resp.json();    
    await appendFileModal(JSON.stringify(data))
}


var  appendFileModal = async function(content) {

    console.log(content);

    const modalElement = document.getElementById('fileModalContent');
    const modalBody = modalElement.querySelector('.modal-body');
    modalBody.innerHTML = content.replace(/&&/g, '<br>').replace(/"/g, ''); // Reemplaza saltos de línea por <br>
    

    const modal = new bootstrap.Modal(modalElement);
    modal.show();

    /*
    var modalContentEl = document.getElementById("fileModalContent");
    modalContentEl.innerText = content; 
    new bootstrap.Modal(document.getElementById("fileModalContent")).show();
    */
    
}


const procesarFicheroGet = async function(theFile){
    const resp = await fetch(`/api/actualizarFromFile?nombre_fichero=${encodeURIComponent(theFile)}`);
    const data = await resp.json();
    appendAlert('Fichero '+ theFile +' actualizado correctamente', 'success')
}


var procesarFichero = async function(theFile){
    const resp = await fetch(`/api/actualizarFromFile`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre_fichero: theFile })
    });

    const data = await resp.json();
    // procesar data...
    appendAlert('Fichero '+ theFile +' actualizado correctamente', 'success')
}

getFicheros();
