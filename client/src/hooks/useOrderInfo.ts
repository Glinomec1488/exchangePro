import { useEffect, useState } from "react"
import { useNavigate, useParams } from "react-router-dom"
import { serveUrl } from "../config"
import { useAppDispatch, useAppSelector } from "../store/hooks"
import { dispatchOrder } from "../store/slices/exchange"

const useOrderInfo = () => {
    const { orderId } = useParams()

    const order = useAppSelector(state => state.exchange.orderInfo)
    const dispatch = useAppDispatch()
    const navigate = useNavigate()

    const getOrder = async () => {
        const order = await fetch(`${serveUrl}/order/${orderId}`).then(res => res.json())

        if (order.error) {
            navigate('/')
        }

        dispatch(dispatchOrder(order))
    }

    const confirmOrder = async () => {
        try {
            await fetch(`${serveUrl}/confirm/${orderId}`, {
                method: 'POST'
            }).then(res => res.json())
            window.location.reload()
        } catch (error: any) {
            console.error(error.message)
        }
    }

    useEffect(() => {
        if (!order) {
            getOrder()
        }
    }, [orderId])

    return {
        orderInfo: order,
        orderId,
        confirmOrder,
    }
}

export default useOrderInfo