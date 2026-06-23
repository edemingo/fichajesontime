
const alertPlaceholder = document.getElementById('liveAlertPlaceholder')

const appendAlert = (message, type) => {
  const wrapper = document.createElement('div')
  wrapper.innerHTML = [
    `<div class="alert alert-${type} alert-dismissible" role="alert" style="position:fixed; right:0px;">`,
    `   <div>${message}</div>`,
    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
    '</div>'
  ].join('')

  alertPlaceholder.append(wrapper)

  setTimeout(() => {
    // Opción usando Bootstrap (Fácil y con animación bonita)
    const alertInstance = bootstrap.Alert.getOrCreateInstance(wrapper.firstElementChild)
    alertInstance.close()
    
    // Nota: El método .close() de Bootstrap destruye automáticamente el "wrapper" del DOM 
    // una vez que termina la animación de ocultado.
  }, 3000)
}


const alertTrigger = document.getElementById('liveAlertBtn')
