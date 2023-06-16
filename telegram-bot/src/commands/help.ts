import { Context } from 'telegraf';

export function helpCommand(ctx: Context) {
    const helpMessage = 'Estos son los comandos disponibles:\n\n' +
        '/help - Muestra la lista de comandos disponibles\n' +
        '/login - Inicia sesión con usuario y contraseña. Ej: "/login miNombreDeusuario miContraseña"' +
        '/logout - Cerra sesión' +
        '/createEvent - Muestra la lista de comandos disponibles\n' +
        '/viewEvents - Muestra la lista de comandos disponibles\n' +
        '/joinEvent - Permite unirse a un evento.\n';
    ctx.reply(helpMessage);
}