import { ICurrency } from "../interfaces"
import { getEnv } from "../utils"

export const chechUserId = async () => {
    try {
        const userId = localStorage.getItem('userId')

        const url = getEnv(process.env.REACT_APP_SERVER_URL, 'REACT_APP_SERVER_URL')
        const serverUserId = await fetch(`${url}/user/${userId || 'null'}`).then(res => res.json())

        localStorage.setItem('userId', serverUserId.id || null)
    } catch (error: any) {
        console.error('chechUserId: ' + error.message)
    }
}

export const wait = (ms: number) => {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve('dd')
        }, ms)
    })
}

export const cutAddress = (address: string) => {
    const start = address.slice(0, 7)
    const end = address.slice(-5)
    return `${start}...${end}`
}

export const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
}

export const getCurrencies = async () => {
    try {
        const url = getEnv(process.env.REACT_APP_SERVER_URL, 'REACT_APP_SERVER_URL')
        const currencies: ICurrency[] = await fetch(`${url}/coins`).then(res => res.json())

        return currencies
    } catch (error: any) {
        console.error(error.message)
    }
}