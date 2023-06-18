import { Context, Scenes } from "telegraf";

interface MyWizzardSession extends Scenes.WizardSessionData {
  event: EventToCreate
}

export interface SessionData extends  Scenes.WizardSession<MyWizzardSession>{
    token?: string | null;
}

export interface AuthContext extends Context {
    session: SessionData;

    // declare scene type
    scene: Scenes.SceneContextScene<AuthContext, MyWizzardSession>;
    // declare wizard type
    wizard: Scenes.WizardContextWizard<AuthContext>;
}

export interface EventToCreate {
    title: string
    description: string
    location: string
    options: HourRequest[]
  }
  
  export interface HourRequest {
    date: string
    hour: number
    minute: number
  }

  export interface Event {
    id: string
    organizer: string
    voting: boolean
    title: string
    description: string
    location: string
    date: string
    guests: string[]
    options: Option[]
  }
  
  export interface Option {
    date: string
    votes: string[]
  }