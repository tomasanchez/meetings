import { MiddlewareFn } from "telegraf";
import { AuthContext } from "../models/models";

// Middleware de autenticación
export const isAuthenticated: MiddlewareFn<AuthContext> = async (ctx, next) => {
    if (!ctx.session.token) {
      // El usuario no está autenticado, puedes enviar un mensaje de error o realizar alguna acción adecuada
      return ctx.reply('Debes iniciar sesión para realizar esta acción.');
    }

    // El usuario está autenticado, continúa con la siguiente función o middleware
    return next();
  };