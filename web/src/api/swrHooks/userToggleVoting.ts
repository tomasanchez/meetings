import useSWR from "swr";
import { ToggleVotingRequest } from "../models/dataApi";
import { fetcher } from "../fetcher";


export default function useToggleVoting(id: string) {
    const { data, mutate, error, isLoading } = useSWR<ToggleVotingRequest>(`scheduler-service/schedules/${id}/voting`, fetcher);

    return {
        event: data,
        mutate,
        error,
        isLoading
    };
}