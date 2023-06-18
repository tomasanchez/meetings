import axios from "axios";
import { Context } from "telegraf";
import { Event } from '../models/models'

export async function viewEvents(ctx: Context) {
  try {
    // Realizar la solicitud GET utilizando Axios con async/await
    const response = await axios.get("http://localhost:8080/api/v1/" + 'schedules')

    // La solicitud se realizó correctamente, puedes manejar la respuesta aquí
    console.log('Eventos recibidos correctamente', response.data);
    let data = response.data.data;
    let returnMessage = "";
    console.log(data[0].options);
    
    if(data && data.length){
      returnMessage += 'Estos son los siguientes eventos:\n';
      data.forEach((event: Event) => {
      returnMessage +=
      `Id: ${event.id} (Usalo para unirte)
    Organizador: ${event.organizer}
    Votacion: ${event.voting ? 'Abierta' : 'Cerrada'}
    Titulo: ${event.title}
    Descripcion: ${event.description}
    Locacion: ${event.location}\n`
    returnMessage += ("Invitados: " + (event.guests.length > 0 ? event.guests.toString() : 'No hay invitados') + "\n");
    returnMessage += "Opciones: ";
    event.options.forEach((option) => {returnMessage += `${option.date} (x${option.votes.length}), `});
    returnMessage += "\n\n";
  });
    } else {
      returnMessage += 'No hay eventos.';
    }

    ctx.reply(returnMessage);
  } catch (error) {
      throw error
  }
}