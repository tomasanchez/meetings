import axios, { AxiosError } from "axios";

interface SuccessResponse {
    data: {
        token: string;
        type: string;
    };
}

export interface ErrorValidationResponse {
    detail: [{ loc: [string]; msg: string; type: string }];
}

export interface UserNotFoundError {
    detail: string;
}


export async function login(username: string, password: string, ctx: any): Promise<string | null> {
    try {
      const response = await axios.post<SuccessResponse>(process.env.API_URL! + 'auth/token', {
        username,
        password,
      });
  
      if (response.status === 200) {
        const { token } = response.data.data;
        return token;
      } 
      return null
    } catch (error) {
        if (axios.isAxiosError(error)) {
          // El error es específico de Axios (problema de red, código de estado no exitoso, etc.)
          const axiosError: AxiosError<ErrorValidationResponse | UserNotFoundError> = error;
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
        }
        return null
      }
  }
