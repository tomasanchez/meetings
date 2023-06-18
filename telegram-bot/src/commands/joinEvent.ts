import axios, { AxiosError } from "axios";
import { Context } from "telegraf";

export interface EventNotFoundError {
  detail: string;
}

export async function joinEvent(id: String, username: String, ctx: Context) {
  try {
    // Realizar la solicitud GET utilizando Axios con async/await
    const response = await axios.patch("http://localhost:8080/api/v1/" + id + '/relationships/guests', {username});

    // La solicitud se realizó correctamente, puedes manejar la respuesta aquí
    console.log('Response recibida correctamente', response.data);

    if(response.data.status === 200) {
      ctx.reply('Se ha unido al evento con exito!');
    }

  } catch (error) {
    if (axios.isAxiosError(error)) {
      // El error es específico de Axios (problema de red, código de estado no exitoso, etc.)
      const axiosError: AxiosError<EventNotFoundError> = error;
        if (axiosError.response) {
        const responseData = axiosError.response
        if ('detail' in responseData && typeof responseData.detail === 'string') {
          // Manejar el caso de usuario no encontrado
          ctx.reply(responseData.detail)
        } else {
          ctx.reply('Valida que cumpla los requisitos')
        }
      } else {
        // Otro tipo de error de Axios
        console.log(axiosError.message);
      }
    }  }
}