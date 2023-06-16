import { Telegraf, Context, session } from 'telegraf';
import { helpCommand } from './commands/help';
import * as dotenv from 'dotenv';
import { login } from './commands/login';


dotenv.config();


interface SessionData {
  token: string | null;
}

interface AuthContext extends Context {
  session: SessionData;
}

const bot = new Telegraf<AuthContext>(process.env.TOKEN!);

let token: string | null = null

bot.use(session());


bot.start((ctx) => {
  ctx.reply('¡Bienvenido al bot! Para comenzar, puedes usar el comando /help para obtener ayuda.');
});

bot.command('help', helpCommand);

bot.command('login', async (ctx) => {

  const username = ctx.message.text.split(' ')[1]; // Obtiene el usuario del comando
  const password = ctx.message.text.split(' ')[2]; // Obtiene la contraseña del comando

  if (username && password) {
    token = await login(username, password, ctx);
    if (token) ctx.reply('Te has loggeado con exito')

  } else {
    ctx.reply('Verifica de ingresar el usuario y contraseña de la forma indicada.')
  }
});

bot.command('logout', async (ctx) => {

  token = null
  ctx.reply('Te has deslogueado con exito')

});

bot.launch().then(() => {
  console.log('El bot se ha iniciado correctamente.');
});