import axios from 'axios'
const baseURL = 'http://localhost:8000/'

const service = axios.create({
    baseURL: baseURL,
    timeout: 10000,
    headers: {'Content-Type': 'application/json', 'Accept': 'application/json'}
})

class Service {
    constructor() {
        this.fetch = service
    }

    get = async (endpoint) => {
        let respObj = {status: 0, data: null}
        try {
            const response = await this.fetch.get(endpoint)
            respObj.status = response.status
            respObj.data = response.data
        }
        catch(error) {
            if (error.response) {
                respObj.status = error.response.status
                respObj.data = error.response.data
            }
        }
        return respObj
    };

    post = async (endpoint, body) => {
        let respObj = {status: 0, data: null}
        try {
            const response = await this.fetch.post(endpoint, body)
            respObj.status = response.status
            respObj.data = response.data
        }
        catch(error) {
            if (error.response) {
                respObj.status = error.response.status
                respObj.data = error.response.data
            }
        }
        return respObj
    };

    put = async (endpoint, body) => {
        let respObj = {status: 0, data: null}
        const headers = {'Content-Type': "application/x-www-form-urlencoded"}
        try {
            const response = await this.fetch.put(endpoint, body, {headers: headers})
            respObj.status = response.status
            respObj.data = response.data
        }
        catch(error) {
            if (error.response) {
                respObj.status = error.response.status
                respObj.data = error.response.data
            }
        }
        return respObj
    };
}

export default Service;