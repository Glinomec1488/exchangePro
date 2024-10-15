import { useState, useEffect } from 'react'
import { getEnv } from '../../../../utils'

const url = getEnv(process.env.REACT_APP_SERVER_URL, 'REACT_APP_SERVER_URL')

export interface IHistoryItem {
    block: string,
    fromm: string,
    to: string,
    txHash: string,
    value: string,
}

const useHistory = () => {
    const [history, setHistory] = useState<IHistoryItem[]>([])

    const getHistory = async () => {
        try {
            const historyRes: IHistoryItem[] = await fetch(`${url}/transactions`).then(res => res.json())
            setHistory(historyRes.map(elem => (
                {
                    txHash: elem.txHash,
                    block: elem.block,
                    fromm: elem.fromm,
                    to: elem.to,
                    value: elem.value
                }
            )))
        } catch (error: any) {
            console.error(error.message)
        }
    }

    useEffect(() => {
        if (history.length === 0) getHistory()
    })

    useEffect(() => {
        const timer = setInterval(() => {
            fetch(`${url}/genTrans`)
                .then(res => res.json())
                .then(res => {
                    const slicedHistory = history.slice(0, -1)
                    setHistory([
                        {
                            txHash: res.txHash,
                            block: res.block,
                            fromm: res.fromAddress,
                            to: res.to,
                            value: res.value
                        },
                        ...slicedHistory
                    ])
                })
        }, 5000)

        return () => {
            clearInterval(timer)
        }
    })

    return {
        history
    }
}

export default useHistory