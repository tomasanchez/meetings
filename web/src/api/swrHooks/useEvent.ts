import useSWR from "swr";
import { Events } from "../models/dataApi";
import { fetcher } from "../fetcher";


export default function useEvent() {
  const { data, mutate, error, isLoading } = useSWR<Events>("scheduler-service/schedules", fetcher);

  return {
    events: data,
    mutate,
    error,
    isLoading
  };
}

