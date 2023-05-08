import useSWR from "swr";
import { EventWithId } from "../models/dataApi";
import { fetcher } from "../fetcher";


export default function useEventWithId(id: string) {
    const { data, mutate, error, isLoading } = useSWR<EventWithId>(`scheduler-service/schedules/${id}`, fetcher);

    return {
        event: data,
        mutate,
        error,
        isLoading
    };
}