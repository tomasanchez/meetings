import axios, { AxiosError } from "axios";
import { Context } from "telegraf";
import { EventNotFoundError, Option } from '../models/models'

export async function viewEvent(id: String, ctx: Context) {
  try {
    // Realizar la solicitud GET utilizando Axios con async/await
    const response = await axios.get(process.env.API_URL! + 'schedules/' + id);

    // La solicitud se realizó correctamente, puedes manejar la respuesta aquí
    console.log('Evento recibido correctamente', response.data);
    let data = response.data.data;
    let returnMessage =`Id: ${data.id} (Usalo para unirte)
    Organizador: ${data.organizer}
    Votacion: ${data.voting ? 'Abierta' : 'Cerrada'}
    Titulo: ${data.title}
    Descripcion: ${data.description}
    Locacion: ${data.location}\n`
    returnMessage += ("Invitados: " + (data.guests.length > 0 ? data.guests.toString() : 'No hay invitados') + "\n");
    returnMessage += "Opciones: ";
    data.options.forEach((option: Option) => {returnMessage += `${option.date} (x${option.votes.length}), `});
    returnMessage += "\n\n";
    ctx.reply(returnMessage);
  } catch (error) {
    if (axios.isAxiosError(error)) {
      // El error es específico de Axios (problema de red, código de estado no exitoso, etc.)
      const axiosError: AxiosError<EventNotFoundError> = error;
        if (axiosError.response) {
        const responseData = axiosError.response
        console.log(responseData);
        if ('detail' in responseData.data && typeof responseData.data.detail.message === 'string') {
          // Manejar el caso de usuario no encontrado
          ctx.reply(responseData.data.detail.message)
        } else {
          ctx.reply('Valida que cumpla los requisitos')
        }
      } else {
        // Otro tipo de error de Axios
        console.log(axiosError.message);
      }  
    }
  }
}