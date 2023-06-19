import Swal from "sweetalert2"
import ResponseError from "./models/dataApi"

export const fetcher = async (input: RequestInfo | URL, init?: RequestInit | undefined): Promise<any> => {
    try {
        const url = import.meta.env["VITE_URL"];

        let fetchUrl = new URL(url + input)

        const res = await fetch(fetchUrl, init)

        if (!res.ok) {
            console.error(res)
            const error = new ResponseError('An errDor occurred while fetching the data.')
            // Attach extra info to the error object.
            error.info = await res.json()
            error.status = res.status
            throw error
        }

        return res.json()
    } catch (error) {
        Swal.fire({
            title: 'Error',
            text: error.info.detail ?? error.message ?? '[API] An unexpected error occurred',
            icon: 'error',
            confirmButtonText: 'OK'
        });
        throw error;
    }
}