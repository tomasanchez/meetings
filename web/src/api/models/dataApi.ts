export interface RegisterRequest {
    username: string
    email: string
    password: string
    role: string
}

export interface RegisterResponse {
  data: UserRegistered
}

export interface UserRegistered {
  id: string
  username: string
  email: string
  role: string
  isActive: boolean
}


export interface LoginRequest{
    username: string
    password: string
}





// INTERFACE TO FETCH EVENTS

export interface Events {
  data: Event[]
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


// INTERFACE TO CREATE EVENTS

export interface EventRequest {
  organizer: string
  title: string
  description: string
  location: string
  options: HourRequest[]
  guests: any[]
}

export interface HourRequest {
  date: string
  hour: number
  minute: number
}

//INTERFACE TO FETCH AN EVENT WITH AN ID
export interface EventWrapper {
  data: Event
}


//INTERFACE TO VOTE
interface optionVote {
  date: string
  hour: number
  minute: number
}

export interface VoteRequest {
  username: string
  option: optionVote
}


//INTERFACE TO JOIN AN EVENT
export interface JoinRequest {
  username: string
}

//INTERFACE TO TOGGLE VOTING
export interface ToggleVotingRequest {
  username: string
  voting: boolean
}