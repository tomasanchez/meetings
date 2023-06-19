import { Context } from 'telegraf';

export function helpCommand(ctx: Context) {
    const helpMessage = 'Estos son los comandos disponibles:\n\n' +
        '/help - Muestra la lista de comandos disponibles\n' +
        '/login - Inicia sesión con usuario y contraseña. Ej: "/login miNombreDeusuario miContraseña"\n' +
        '/logout - Cerra sesión\n' +
        '/createEvent - Wizard para crear un evento\n' +
        '/viewEvents - Muestra una lista de eventos\n' +
        '/viewEvent - Permite ver un evento en especifico con el Id.  Ej: "/viewEvent id"\n' +
        '/joinEvent - Permite unirse a un evento especificando el id del evento. Ej: "/joinEvent id"\n';
    ctx.reply(helpMessage);
}