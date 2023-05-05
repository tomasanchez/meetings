export interface RegisterRequest {
    username: string
    email: string
    password: string
    role: string
}

export interface LoginRequest{
    username: string
    password: string
}


export type Events = Event[]

export interface Event {
  id: string
  title: string
  description: string
  location: string
  administrator: Administrator
  listOfGuests: string[]
  votedOption: VotedOption
  listOfOptions: ListOfOption[]
  isClosed: boolean
}

export interface Administrator {
  id: string
  email: string
  password: string
}

export interface VotedOption {
  time: Time
  votes: number
  date: string
}

export interface Time {
  hour: number
  minute: number
  second: number
  nano: number
}

export interface ListOfOption {
  time: Time2
  votes: number
  date: string
}

export interface Time2 {
  hour: number
  minute: number
  second: number
  nano: number
}
