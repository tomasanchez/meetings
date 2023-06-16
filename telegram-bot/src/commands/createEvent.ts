import { Scenes } from "telegraf";
import { AuthContext, EventToCreate } from "../models/models";
import axios from "axios";


async function eventCreate(event: EventToCreate, token: string) {

    // Configurar los encabezados de la solicitud
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };


    try {
        // Realizar la solicitud POST utilizando Axios con async/await
        const response = await axios.post(process.env.API_URL! + 'schedules', event, { headers });

        // La solicitud se realizó correctamente, puedes manejar la respuesta aquí
        console.log('Evento creado con éxito:', response.data);
        return response
    } catch (error) {
        throw error
    }

}

export const eventWizard = new Scenes.WizardScene(
    'create-event',
    async (ctx: AuthContext) => {
        await ctx.reply('Paso 1: Por favor, proporciona el titulo del evento. Ej: "Juntada"');
        return ctx.wizard.next();
    },
    async (ctx: AuthContext) => {
        if ('text' in ctx.message!) {
            ctx.scene.session.event = { ...ctx.scene.session.event, title: ctx.message!.text }
        }
        await ctx.reply('Paso 2: Ahora, proporciona la descripción del evento. Ej: "Nos juntamos a tomar un cafe"');
        return ctx.wizard.next();
    },
    async (ctx: AuthContext) => {
        if ('text' in ctx.message!) {
            ctx.scene.session.event = { ...ctx.scene.session.event, description: ctx.message!.text }
        }
        await ctx.reply('Paso 3: Ahora, proporciona la ubicación del evento. Ej: "Av Rivadavia 1234"');
        return ctx.wizard.next();
    },
    async (ctx: AuthContext) => {
        if ('text' in ctx.message!) {
            ctx.scene.session.event = { ...ctx.scene.session.event, location: ctx.message!.text }
        }
        await ctx.reply("Último paso: Indicanos que fecha te gustaría. Ej: 'AAAA-MM-DD HH:mm'");
        return ctx.wizard.next();
    },
    async (ctx: AuthContext) => {
        if ('text' in ctx.message!) {
            ctx.scene.session.event = { ...ctx.scene.session.event, options: [{ date: '2023-01-01', hour: 10, minute: 20 }] }
        }


        try {
            await eventCreate(ctx.scene.session.event, ctx.session.token!)
            const responseText = `¡Evento creado con éxito! ${ctx.scene.session.event.description} ${ctx.scene.session.event.title}`;
            await ctx.reply(responseText);

        } catch (error) {
            console.log(error)
        }
        return ctx.scene.leave();
    }
);