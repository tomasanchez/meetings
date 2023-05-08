import useSWR from "swr";
import { JoinRequest, VoteRequest } from "../models/dataApi";
import { fetcher } from "../fetcher";


export default function useJoinEvent(id: string) {
    const { data, mutate, error, isLoading } = useSWR<JoinRequest>(`scheduler-service/schedules/${id}/relatiuonships/guests`, fetcher);

    return {
        event: data,
        mutate,
        error,
        isLoading
    };
}