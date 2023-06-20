import axios, { AxiosError } from "axios";
import { Context } from "telegraf";
import { EventNotFoundError } from "../models/models";

interface Token {
  email: string;
  exp: number;
  id: string;
  role: string;
  username: string;
}

export async function joinEvent(id: String, token: String, ctx: Context) {
  try {
  // Configurar los encabezados de la solicitud
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  };

  const decodedToken: Token = JSON.parse(Buffer.from(token.split('.')[1], 'base64').toString());
  const username: String = decodedToken.username;
  
  console.log(id, username);
  // Realizar la solicitud PATCH utilizando Axios con async/await
  const response = await axios.patch(process.env.API_URL! + "schedules/" + id + '/relationships/guests', {username}, {headers});
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
    }  }
}