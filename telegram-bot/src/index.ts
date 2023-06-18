import { Scenes, Telegraf,session } from 'telegraf';
import * as dotenv from 'dotenv';
import { isAuthenticated } from './middleware/isAuthenticated';
import { AuthContext } from './models/models';
import {  eventWizard, helpCommand, login, viewEvents, joinEvent } from './commands';

dotenv.config();

const stage = new Scenes.Stage<any>([eventWizard]);
const bot = new Telegraf<AuthContext>(process.env.TOKEN!);

bot.use(session(), stage.middleware());


bot.start((ctx) => {
  ctx.reply('¡Bienvenido al bot! Para comenzar, puedes usar el comando /help para obtener ayuda.');
});

bot.command('help', helpCommand);

bot.command('login', async (ctx) => {

  const username = ctx.message.text.split(' ')[1]; // Obtiene el usuario del comando
  const password = ctx.message.text.split(' ')[2]; // Obtiene la contraseña del comando

  if (username && password) {
    const token = await login(username, password, ctx);

    if (token) {
      ctx.session!.token = token;
      ctx.reply('Te has loggeado con exito')}

  } else {
    ctx.reply('Verifica de ingresar el usuario y contraseña de la forma indicada.')
  }
});

bot.command('createEvent', isAuthenticated, ctx => ctx.scene.enter('create-event'))

bot.command('viewEvents', isAuthenticated, viewEvents);

bot.command('joinEvent', isAuthenticated, async (ctx) => {
  const id = ctx.message.text.split(' ')[1];
  const username = ctx.message.text.split(' ')[2];
  await joinEvent(id, username, ctx);
})

bot.command('logout', isAuthenticated ,  async (ctx) => {

  ctx.session.token = null
  ctx.reply('Te has deslogueado con exito')

});


bot.launch().then(() => {
  console.log('El bot se ha iniciado correctamente.');
});