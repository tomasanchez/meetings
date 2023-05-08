import useSWR from "swr";
import { VoteRequest } from "../models/dataApi";
import { fetcher } from "../fetcher";


export default function useEventVote(id: string) {
    const { data, mutate, error, isLoading } = useSWR<VoteRequest>(`scheduler-service/schedules/${id}/options`, fetcher);

    return {
        event: data,
        mutate,
        error,
        isLoading
    };
}